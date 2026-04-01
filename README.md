# Home Assistant Greenchoice Sensor

[![hacs][hacs-badge]][hacs-url]
[![release][release-badge]][release-url]
![downloads][downloads-badge]

This is a Home Assistant custom component that connects to the Greenchoice API to retrieve current usage and pricing
data. The integration refreshes every hour and provides both daily meter readings and hourly energy statistics for use
in the Energy dashboard.

## Installation

### HACS Installation (Recommended)

1. Add this repository URL as a custom repository in HACS and label it as an integration
2. Install the "Greenchoice" integration via HACS
3. Restart Home Assistant
4. Go to **Settings** > **Devices & Services** > **Add Integration**
5. Search for "Greenchoice" and follow the configuration steps

### Manual Installation

1. Place the `greenchoice` folder in your `custom_components` directory
2. Restart Home Assistant
3. Go to **Settings** > **Devices & Services** > **Add Integration**
4. Search for "Greenchoice" and follow the configuration steps

## Configuration

The integration uses Home Assistant's config flow for easy setup through the UI.

### Basic Setup

1. Go to **Settings** > **Devices & Services**
2. Click **Add Integration** and search for "Greenchoice"
3. Enter your Greenchoice credentials:
    - **Email**: Your Greenchoice login email
    - **Password**: Your Greenchoice password
4. Select your contract address from the options. Optionally fill in:
    - **Sensor Name**: Custom name for this instance (optional, defaults to "Greenchoice")

### Multiple Contracts

You can add multiple Greenchoice integrations for different contracts or accounts:

1. Repeat the setup process for each contract
2. Use different names to distinguish between them (e.g., "House Energy", "Solar System")
3. Each integration will create its own set of sensors with the custom name as prefix

## Sensors Created

Each integration instance creates the following sensors:

### Daily Meter Readings

These sensors reflect the most recent daily meter reading from Greenchoice (typically delayed by 1–2 days). The date
of the reading is available as a sensor attribute.

- **Electricity Consumption Off Peak** (kWh) - Low tariff consumption
- **Electricity Consumption Normal** (kWh) - Normal/peak tariff consumption
- **Electricity Consumption Total** (kWh) - Total electricity consumed
- **Electricity Feed In Off Peak** (kWh) - Low tariff feed-in to grid
- **Electricity Feed In Normal** (kWh) - Normal/peak tariff feed-in to grid
- **Electricity Feed In Total** (kWh) - Total electricity fed back to grid
- **Gas Consumption** (m³) - Gas consumption

### Electricity & Gas Pricing

- **Electricity Price Single** (€/kWh) - Single rate electricity price
- **Electricity Price Off Peak** (€/kWh) - Low tariff electricity price
- **Electricity Price Normal** (€/kWh) - Normal/peak tariff electricity price
- **Electricity Feed In Compensation** (€/kWh) - Compensation rate for fed-in electricity
- **Electricity Feed In Cost** (€/kWh) - Cost/fee for feeding electricity back
- **Gas Price** (€/m³) - Gas price per cubic meter

### Hourly Statistics (Energy Dashboard)

In addition to the daily sensors, the integration automatically imports **hourly** consumption data into Home
Assistant's recorder statistics. This makes your energy usage visible at the per-hour granularity in the
**Energy dashboard**.

Three statistics series are created per integration instance:

| Sensor                           | Unit | Description                                   |
|----------------------------------|------|-----------------------------------------------|
| Electricity consumption (hourly) | kWh  | Electricity delivered from the grid, per hour |
| Electricity feed-in (hourly)     | kWh  | Electricity fed back to the grid, per hour    |
| Gas consumption (hourly)         | m³   | Gas consumed, per hour                        |

Hourly data is imported automatically on each refresh cycle. The integration also self-heals: if data is missing for
up to 7 days (e.g. after an internet outage), the gaps are backfilled on the next successful refresh.

> **Note:** Yesterday's data is only imported after 13:00 local time to allow Greenchoice time to publish it.

## Services

### `greenchoice.reimport_hourly_statistics`

Force a full reimport of hourly statistics starting from a given date up to and including yesterday. Use this to
fix gaps, negative spikes, or other artefacts in the Energy dashboard.

| Field        | Type | Required | Description                                                                                                |
|--------------|------|----------|------------------------------------------------------------------------------------------------------------|
| `start_date` | date | yes      | The first day to reimport (inclusive). All days through yesterday are fetched and written to the recorder. |

**Example:**

```yaml
service: greenchoice.reimport_hourly_statistics
data:
  start_date: "2026-03-01"
```

## Troubleshooting

- The integration logs under the `greenchoice` domain. Enable debug logging for detailed output:

```yaml
logger:
  logs:
    custom_components.greenchoice: debug
```

- If hourly statistics look wrong in the Energy dashboard, use the `reimport_hourly_statistics` service to
  rewrite the affected date range.

For issues or feature requests, please use the GitHub repository.

<!-- Badges -->

[hacs-url]: https://github.com/hacs/integration

[hacs-badge]: https://img.shields.io/badge/hacs-default-orange.svg?style=flat-square

[release-url]: https://github.com/barisdemirdelen/homeassistant-greenchoice/releases

[release-badge]: https://img.shields.io/github/v/release/barisdemirdelen/homeassistant-greenchoice?style=flat-square

[downloads-badge]: https://img.shields.io/github/downloads/barisdemirdelen/homeassistant-greenchoice/total?style=flat-square
