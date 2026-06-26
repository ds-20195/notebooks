Notebooks for Friday labs are in the main repo.  When moved here, they are considered *published*.

The drafts folder contains notebooks-in-progress, which are subject to change before they are published!

# INDEX

[warmup](Notebook0.ipynb) - Basic concepts from Python and Pandas

## Part I: Intro to census and geography

[Week 1](Notebook1.ipynb) - Introduction to Census data
- Census tables, categories, dataframe operations, Matplotlib 

[Week 2](Notebook2.ipynb) - Decennial census, ACS
- geography hierarchy, central spine, power laws, ACS socioeconomic variables, boxplots, table joins

[Week 3](Notebook3.ipynb) - Managing geographies
- geodataframes, map projection and CRS, precincts and election data, MAUP and proration


## Part II: How things move

[Week 4](Notebook4.ipynb) - Migration and relocation
- ACS county flows, graphs, NetworkX, FlowmapBlue, microdata with national origins, PUMS and PUMAs

[Week 5](Notebook5.ipynb) - Organ donation
- OPTN data for kidney and liver donation, hospital-to-hospital flows, KDEs, logistic regression, spatial indexing

[Week 6](Notebook6.ipynb) - Cities and transit
- NYC Open Data, dissolves and buffers, isochrones, OSMnx and network distance

## Part III: Where we live 

[Week 7](Notebook7.ipynb) - Incarceration and policing
- VERA ncarceration data, police incident/arrest data in SF and Chicago, dynamic heatmaps in Folium

[Week 8](Notebook8.ipynb) - Evictions and redlining
- HRI (Historical Redlining Index), Princeton Eviction Lab data, proprietary and modeled data, comparison to NYC Open Data

[Week 9](Notebook9.ipynb) - Neighborhoods and communities
- NYT neighborhood mapping project, Communities of Interest dataset, participatory mapping


--- 
# **CHANGES TO THE CENSUS API** 

On 12 May 2026, the Census announced that all requests to its API will now require an API
key. Previous versions (<= 0.8.26) of the `census` package contained a bug that would not pass 
the API key included in the creation of a `Census` class to requests. This was fixed in
release of version 0.8.27 on 16 May 2026, but some students may still be working with an older
version of the package. In the event that you are, replace the line

```python
from census import Census
```

with the following drop-in patch:

```python
from census import Census

# The logic fixes an error caused by the Census changing its API requirement on 12 May 2026. 
# The Census package did not properly pass the API key to all requests, so we have to patch the 
# elements that handle that logic.
from functools import lru_cache
from census.core import Client, supported_years


def _patched_field_type(self, field, year):
    url = self.definition_url % (year, self.dataset, field)
    resp = self.session.get(url, params={"key": self._key})

    type_map = {
        "fips-for": str,
        "fips-in": str,
        "int": float,
        "long": float,
        "float": float,
        "string": str,
    }
    if resp.status_code == 200:
        try:
            predicate_type = resp.json().get("predicateType", "string")
            return type_map.get(predicate_type, str)
        except Exception:
            return str
    return str


def _patched_tables(self, year=None):
    if year is None:
        year = self.default_year
    tables_url = self.groups_url % (year, self.dataset)
    resp = self.session.get(tables_url, params={"key": self._key})
    return resp.json()["groups"]


@supported_years()
def _patched_fields(self, year=None, flat=False):
    if year is None:
        year = self.default_year

    data = {}
    fields_url = self.definitions_url % (year, self.dataset)
    resp = self.session.get(fields_url, params={"key": self._key})
    obj = resp.json()

    if flat:
        for key, elem in obj["variables"].items():
            if key in ["for", "in"]:
                continue
            data[key] = "{}: {}".format(
                elem.get("concept", ""), elem.get("label", "")
            )
    else:
        data = obj["variables"]
        data.pop("for", None)
        data.pop("in", None)
    return data


Client._field_type = lru_cache(maxsize=1024)(_patched_field_type)
Client.tables = _patched_tables
Client.fields = _patched_fields
```
