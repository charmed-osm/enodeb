# charm-simple-native

This is an example of a simple native charm used by Open Source Mano (OSM), written in the [Python Operator Framwork](https://github.com/canonical/operator)


## Usage

To get the charm:
```bash
git clone https://github.com/charmed-osm/charm-simple-native
cd charm-simple-native
# Install the submodules
git submodule update --init
```

To deploy to juju:
```
juju deploy .
```

```
# Make sure the charm is in an Active state
juju status
```
