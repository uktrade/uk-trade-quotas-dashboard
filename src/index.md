---
theme: dashboard
title: Quota balances
toc: false
style: style.css
---


```js
const balances = FileAttachment("./data/balances.json").json({typed: true}).then(data => data.map(row => ({
  'date': Date.parse(row.quota_definition__last_allocation_date),
  'percentage_remaining': (1-row.quota_definition__fill_rate)*100,
})));
```

<div class="govuk-width-container">

```js
let govuk_colour_palette = ["#12436D", "#28A197", "#801650", "#F46A25", "#3D3D3D", "#A285D1"] // Ideally use only the first 4, and in the order they appear 

let sorted = balances.sort(function(a,b) {
    return b['date'] - a['date']
});

function balancesChart(data, {width}) {
  return Plot.plot({
    title: "Percentage of quota remaining over time",
    width,
    x: {type: "utc"},
    y: {domain: [0, 100]},
    color: {range:govuk_colour_palette},
    marks: [
      Plot.gridX(),
      Plot.gridY(),
      Plot.dot(data, {x: "date", y: "percentage_remaining"}),
      Plot.line(data, {x: "date", y: "percentage_remaining"})
    ]
  })
}


```

<h1 class="govuk-heading-l govuk-!-margin-top-7">Quota balances ⚖️</h1>

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => balancesChart(sorted, {width}))}
  </div>
</div>


```js
const currentVolumes = FileAttachment("./data/quotas-including-current-volumes.csv").csv({typed: true}).then(data => data.filter(row => ['Open', 'Critical'].includes(row.quota_definition__status)))
```

```js
function remainingChart(data, {width}) {
  return Plot.plot({
    title: "Geographical areas with highest total percentage of remaining open and critical quotas",
    width,
    x: {grid: true, label: "Percentage remaining"},
    y: {label: null},
    marks: [
      Plot.rectX(data, Plot.groupY(
        {x: (values, b) => {
          return Math.max(0, 1 - values.map(row => row.quota_definition__balance).reduce((partialSum, a) => partialSum + a, 0) / values.map(row => row.quota_definition__initial_volume).reduce((partialSum, a) => partialSum + a, 0))
        }},
        {y: "quota__geographical_areas", tip: true, sort: {y: "-x"}, fill: govuk_colour_palette[0]}
      )),
      Plot.ruleX([0]),
      Plot.axisY({label: null, marginLeft: 620}),
    ]
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => remainingChart(currentVolumes, {width}))}
  </div>
</div>


<h1 class="govuk-heading-l govuk-!-margin-top-7">Rocket launches 🚀</h1>

<!-- Load and transform the data -->

```js
const launches = FileAttachment("data/launches.csv").csv({typed: true});
```

<!-- A shared color scale for consistency, sorted by the number of launches -->

```js
const color = Plot.scale({
  color: {
    type: "categorical",
    domain: d3.groupSort(launches, (D) => -D.length, (d) => d.state).filter((d) => d !== "Other"),
    unknown: "var(--theme-foreground-muted)"
  }
});
```

<!-- Cards with big numbers -->

<div class="grid grid-cols-4">
  <div class="card">
    <h2>United States 🇺🇸</h2>
    <span class="big">${launches.filter((d) => d.stateId === "US").length.toLocaleString("en-US")}</span>
  </div>
  <div class="card">
    <h2>Russia 🇷🇺 <span class="muted">/ Soviet Union</span></h2>
    <span class="big">${launches.filter((d) => d.stateId === "SU" || d.stateId === "RU").length.toLocaleString("en-US")}</span>
  </div>
  <div class="card">
    <h2>China 🇨🇳</h2>
    <span class="big">${launches.filter((d) => d.stateId === "CN").length.toLocaleString("en-US")}</span>
  </div>
  <div class="card">
    <h2>Other</h2>
    <span class="big">${launches.filter((d) => d.stateId !== "US" && d.stateId !== "SU" && d.stateId !== "RU" && d.stateId !== "CN").length.toLocaleString("en-US")}</span>
  </div>
</div>

<!-- Plot of launch history -->

```js
function launchTimeline(data, {width} = {}) {
  return Plot.plot({
    title: "Launches over the years",
    width,
    height: 300,
    y: {grid: true, label: "Launches"},
    color: {range:govuk_colour_palette, legend: true},
    marks: [
      Plot.rectY(data, Plot.binX({y: "count"}, {x: "date", fill: "state", interval: "year", tip: true})),
      Plot.ruleY([0])
    ]
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => launchTimeline(launches, {width}))}
  </div>
</div>

<!-- Plot of launch vehicles -->

```js
function vehicleChart(data, {width}) {
  return Plot.plot({
    title: "Popular launch vehicles",
    width,
    height: 300,
    marginTop: 0,
    marginLeft: 50,
    x: {grid: true, label: "Launches"},
    y: {label: null},
    color: {range:govuk_colour_palette, legend: true},
    marks: [
      Plot.rectX(data, Plot.groupY({x: "count"}, {y: "family", fill: "state", tip: true, sort: {y: "-x"}})),
      Plot.ruleX([0])
    ]
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => vehicleChart(launches, {width}))}
  </div>
</div>

Data: Jonathan C. McDowell, [General Catalog of Artificial Space Objects](https://planet4589.org/space/gcat)

<!-- Closes .govuk-width-container -->
</div>
