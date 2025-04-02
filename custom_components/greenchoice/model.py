from __future__ import annotations

import uuid
from datetime import datetime, date
from functools import cached_property
from typing import Iterator

from pydantic import BaseModel, Field, AliasChoices, ConfigDict
from pydantic.alias_generators import to_camel


class CamelCaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)


class Profile(BaseModel):
    """/api/v2/profiles"""

    customerNumber: int
    agreementId: int
    roleName: str
    name: str
    street: str
    houseNumber: int
    houseNumberAddition: int | str | None = None
    postalCode: str
    city: str
    energySupplyStatus: str
    moveInDate: datetime
    hasActiveGasSupply: bool
    hasActiveElectricitySupply: bool
    moveOutDate: datetime | None = None


class PreferencesSubject(BaseModel):
    customerNumber: int
    agreementId: int
    LeveringsStatus: int | None = None


class Preferences(BaseModel):
    """/api/v2/preferences"""

    accountId: uuid.UUID
    subject: PreferencesSubject


class Account(BaseModel):
    """/api/v2/accounts"""

    accountId: uuid.UUID
    email: str
    accountType: str
    firstName: str
    emailModifiedOnUtc: datetime
    accountTypeModifiedOnUtc: datetime
    firstNameModifiedOnUtc: datetime


class ElectricityTariff(BaseModel):
    leveringHoog: float
    leveringLaag: float
    leveringEnkel: float
    leveringHoogBtw: float
    leveringLaagBtw: float
    leveringEnkelBtw: float
    soortMeter: str
    terugLeveringEnkel: float
    terugLeveringHoog: float
    terugLeveringLaag: float
    terugleverVergoeding: float
    terugleverKostenIncBtw: float
    terugleverKostenExcBtw: float
    terugleverKostenBtw: float
    btw: float
    btwPercentage: float
    vastrechtPerDagExcBtw: float
    vastrechtPerDagIncBtw: float
    vastrechtPerDagBtw: float
    netbeheerPerDagExcBtw: float
    netbeheerPerDagIncBtw: float
    netbeheerPerDagBtw: float
    reb: float
    sde: float
    capaciteit: str | None = None
    rebTeruggaveIncBtw: float | None = None
    leveringLaagAllIn: float = Field(
        validation_alias=AliasChoices("leveringLaagAllIn", "leveringLaagAllin")
    )
    leveringHoogAllIn: float = Field(
        validation_alias=AliasChoices("leveringHoogAllIn", "leveringHoogAllin")
    )
    leveringEnkelAllIn: float = Field(
        validation_alias=AliasChoices("leveringEnkelAllIn", "leveringEnkelAllin")
    )


class GasTariff(BaseModel):
    levering: float
    leveringAllIn: float
    leveringBtw: float
    btw: float
    btwPercentage: float
    vastrechtPerDagExcBtw: float
    vastrechtPerDagIncBtw: float
    vastrechtPerDagBtw: float
    netbeheerPerDagExcBtw: float
    netbeheerPerDagIncBtw: float
    netbeheerPerDagBtw: float
    reb: float
    sde: float
    capaciteit: str | None = None


class RatesV1(BaseModel):
    """/api/v2/customers/<customerNumber>/rates
    ?AgreementIdElectricity=<agreementId>
    &AgreementIdGas=<agreementId>
    &HouseNumber=<houseNumber>
    &ReferenceIdElectricity=<refIdElectricity>
    &ReferenceIdGas=<refIdGas>
    &ZipCode=<zipCode>>"""

    beginDatum: datetime
    eindDatum: datetime

    stroom: ElectricityTariff | None = None
    gas: GasTariff | None = None


class UsageDependentElectricityRates(CamelCaseModel):
    all_in_delivery_single_including_vat: float
    delivery_single: float
    all_in_delivery_single_vat: float
    all_in_delivery_low_including_vat: float
    delivery_low: float
    all_in_delivery_low_vat: float
    all_in_delivery_normal_including_vat: float
    delivery_normal: float
    all_in_delivery_normal_vat: float
    energy_tax: float
    sustainable_energy_surcharge: float | None = None
    feed_in_compensation: float | None = None
    feed_in_volume_limit_in_kwh: float | None = None
    feed_in_cost_including_vat: float | None = None
    feed_in_cost_excluding_vat: float | None = None
    feed_in_cost_vat: float | None = None


class UsageDependentGasRates(CamelCaseModel):
    all_in_delivery_including_vat: float
    delivery: float
    all_in_delivery_vat: float
    energy_tax_excluding_vat: float
    energy_tax: float
    sustainable_energy_surcharge: float | None = None


class UsageIndependentRates(CamelCaseModel):
    fixed_charge_per_day_including_vat: float
    fixed_charge_per_day_excluding_vat: float
    fixed_charge_per_day_vat: float
    reduction_energy_tax_including_vat_per_day: float
    grid_operator_rate_per_day_including_vat: float
    grid_operator_rate_per_day_excluding_vat: float
    grid_operator_rate_per_day_vat: float


class ContractRates(CamelCaseModel):
    vat_percentage: float
    usage_dependent_electricity_rates: UsageDependentElectricityRates | None = None
    usage_dependent_gas_rates: UsageDependentGasRates | None = None
    usage_independent_rates: UsageIndependentRates | None = None


class Contract(CamelCaseModel):
    type: str
    display_name: str
    begin_date: date
    end_date: date | None = None
    cancellation_date: date | None = None
    duration_in_months: int | None = None
    product_type: str
    physical_capacity: str
    rates: ContractRates
    rate_type: str
    sub_agreement_id: int


class Rates(CamelCaseModel):
    id: int
    contracts: list[Contract]

    class Request(BaseModel):
        request_url: str = "/api/v2/customers/{customer_number}/agreements/{agreement_id}/contracts/current"

        customer_number: int
        agreement_id: int

        def build_url(self) -> str:
            return self.request_url.format(
                customer_number=self.customer_number, agreement_id=self.agreement_id
            )

    @cached_property
    def electricity(self) -> Contract | None:
        for contract in self.contracts:
            if contract.product_type.upper() == "E":
                return contract
        return None

    @cached_property
    def gas(self) -> Contract | None:
        for contract in self.contracts:
            if contract.product_type.upper() == "G":
                return contract
        return None


class Reading(BaseModel):
    readingDate: datetime
    normalConsumption: float | None = None
    offPeakConsumption: float | None = None
    normalFeedIn: float | None = None
    offPeakFeedIn: float | None = None
    gas: float | None = None


class MeterMonth(BaseModel):
    month: int
    readings: list[Reading]


class MeterProduct(BaseModel):
    productType: str
    months: list[MeterMonth]


class MeterReadings(BaseModel):
    productTypes: list[MeterProduct]

    class Request(BaseModel):
        request_url: str = """/api/v2/customers/{customer_number}/agreements/{agreement_id}/meter-readings/{year}/"""

        customer_number: int
        agreement_id: int
        year: int

        def build_url(self) -> str:
            return self.request_url.format(
                customer_number=self.customer_number,
                agreement_id=self.agreement_id,
                year=self.year,
            )

    @property
    def last_electricity_reading(self) -> Reading | None:
        for last_reading in self.iter_readings("stroom"):
            return last_reading
        return None

    @property
    def last_gas_reading(self) -> Reading | None:
        for last_reading in self.iter_readings("gas"):
            return last_reading
        return None

    def iter_readings(self, product_type) -> Iterator[Reading]:
        for product in self.productTypes:
            if product.productType.lower() != product_type:
                continue
            for month in sorted(product.months, key=lambda p: p.month, reverse=True):
                for reading in sorted(
                    month.readings, key=lambda r: r.readingDate, reverse=True
                ):
                    yield reading
