---
theme: dashboard
title: Quota balances
toc: false
style: style.css
---


```js
const balances = await FileAttachment("./data/balances.json").json({typed: true})

let tableData = []
for (let balanceSet in balances){
    tableData.push(balances[balanceSet].map((row) => {
      return {
        'id':row.quota__order_number,
        'date': Date.parse(row.quota_definition__last_allocation_date),
        'percentage_remaining': (1-row.quota_definition__fill_rate)*100,
      }
    }))
}
```
<div class="govuk-width-container">

```js
let govuk_colour_palette = ["#12436D", "#28A197", "#801650", "#F46A25", "#3D3D3D", "#A285D1"] // Ideally use only the first 4, and in the order they appear 

let sortedBalances=[]
for (let i=0;i < tableData.length;i++){
  sortedBalances.push(tableData[i].toSorted(function(a,b) {
    return b['date'] - a['date']
}));
}
function balancesChart(data, {width}) {
  return Plot.plot({
    title: "Percentage of quota remaining over time",
    width,
    x: {type: "utc"},
    y: {domain: [0, 100]},
    color: {range:govuk_colour_palette,legend: true},
    marks: [
      Plot.gridX(),
      Plot.gridY(),
      Plot.dot(data[0], {x: "date", y: "percentage_remaining",stroke: "id", symbol:'asterisk'}),
      //Plot.line(data[0], {x: "date", y: "percentage_remaining",stroke: "id"}),
      Plot.dot(data[1], {x: "date", y: "percentage_remaining",stroke: "id", symbol:'asterisk'}),
      //Plot.line(data[1], {x: "date", y: "percentage_remaining",stroke: "id"}),
      Plot.dot(data[2], {x: "date", y: "percentage_remaining",stroke: "id", symbol:'asterisk'}),
      //Plot.line(data[2], {x: "date", y: "percentage_remaining",stroke: "id"}),
      Plot.dot(data[3], {x: "date", y: "percentage_remaining",stroke: "id", symbol:'asterisk'}),
      //Plot.line(data[3], {x: "date", y: "percentage_remaining",stroke: "id"}),
    ]
  })
}


```

<h1 class="govuk-heading-l govuk-!-margin-top-7">Quota balances ⚖️</h1>

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => balancesChart(sortedBalances, {width}))}
  </div>
</div>


```js
const currentVolumes = FileAttachment("./data/quotas-including-current-volumes.csv").csv({typed: true}).then(data => data.filter(row => ['Open', 'Critical'].includes(row.quota_definition__status)))
```

```js
function remainingChart(data, {width}) {
  return Plot.plot({
    title: "Areas with highest percentage of unused quotas",
    subtitle: "The 20 geographical areas that have the highest percentage remaining balance of open and critical quotas",
    width,
    x: {grid: true, label: "Percentage remaining", domain: [0, 100]},
    y: {label: null},
    marks: [
      Plot.rectX(data, Plot.groupY(
        {x: (values, b) => {
          return Math.max(0, 1 - values.map(row => row.quota_definition__balance).reduce((partialSum, a) => partialSum + a, 0) / values.map(row => row.quota_definition__initial_volume).reduce((partialSum, a) => partialSum + a, 0)) * 100
        }},
        {y: "quota__geographical_areas", tip: true, sort: {y: "-x", limit: 20}, fill: govuk_colour_palette[0]}
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


Data: Jonathan C. McDowell, [General Catalog of Artificial Space Objects](https://planet4589.org/space/gcat)

<!-- Closes .govuk-width-container -->
</div>
