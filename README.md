# Home Assistant Greenchoice Sensor
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

This is a Home Assistant custom component (sensor) that connects to the Greenchoice API to retrieve current usage data (daily meter data).

The sensor will check every hour if a new reading can be retrieved but Greenchoice practically only gives us one reading a day over this API. The reading is also delayed by 1 or 2 days (this seems to vary). The sensor will give you the date of the reading as an attribute.

### Install:

[//]: # (1. Search for 'greenchoice' in [HACS]&#40;https://hacs.xyz/&#41;. )

[//]: # (    *OR*)
1. Place the 'greenchoice' folder in your 'custom_compontents' directory if it exists or create a new one under your config directory.
2. Add your username and password to the secrets.yaml:

```YAML
greenchoicepass: your_secret_password
greenchoiceuser: your@user.name
```

3. Restart Home Assistant to make it load the integration.
4. Finally add the component to your configuration.yaml, an example of a proper config entry:

```YAML
sensor:
  - platform: greenchoice
    name: meter_readings
    password: !secret greenchoicepass
    username: !secret greenchoiceuser
```

### Specifying Agreement Id

By default, this sensor uses the preferred agreement id for the user. This is what you normally see when you open `https://mijn.greenchoice.nl/`
If you would like to gather results for a specific agreement id, you can fill in the optional `customer_number` and `agreement_id` config values.

You can check what your currently preferred customer number and agreement id is with this url: `https://mijn.greenchoice.nl/api/v2/preferences`
To find all your customer numbers and agreement ids you can use this url: `https://mijn.greenchoice.nl/api/v2/profiles`


```YAML
sensor:
  - platform: greenchoice
    name: meter_readings
    password: !secret greenchoicepass
    username: !secret greenchoiceuser
    customer_number: 12341234
    agreement_id: 56785678
```

### Gathering data for multiple contracts:

You can also gather data for multiple contracts, by using multiple copies of this sensor. Here is an example configuration:

```YAML
sensor:
  - platform: greenchoice
    name: greenchoice_user1
    password: !secret greenchoicepass1
    username: !secret greenchoiceuser1
  - platform: greenchoice
    name: greenchoice_user2_agreement1
    password: !secret greenchoicepass2
    username: !secret greenchoiceuser2
    customer_number: 12341234
    agreement_id: 11111111
  - platform: greenchoice
    name: greenchoice_user2_agreement2
    password: !secret greenchoicepass2
    username: !secret greenchoiceuser2
    customer_number: 12341234
    agreement_id: 22222222
```