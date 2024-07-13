---
# Notes to maintainers:
#
# 1. It's probably good to read the following before attempting changes:
#    https://observablehq.com/framework/markdown
#    https://observablehq.com/framework/javascript
#    https://observablehq.com/framework/reactivity
#    https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise
#
# 2. We use quite a lot of HTML to leverage the GOV.UK Design System, more than most Observable
#    Framework examples, which means you probably want to add blank lines for readability. But be
#    careful! In normal HTML this has no effect, but here it runs the risk of being parsed as
#    Markdown, and if too intented will be treated as a code block to display.
#
#    We have worked around this by using empty HTML comments <-- --> to add in some whitespace.

# Title is empty since this is a single page site, and the <title> element will contain the site name
title: 
toc: false
theme: air
---

```js
const stringToCodeMap = {
  "050096 Food preparation (US)":"050096",
  "050097 Wine (ERGA OMNES)":"050097",
  "050120 Sausages (ERGA OMNES)":"050120",
  "050212 Fruits/Nuts (Turkey)":"050212",
  "050035 Dried vegetables (ERGA OMNES)": "050035",
  "050232 Pasta (Turkey)": "050232",
};
const govuk_colour_palette = ["#12436D", "#28A197", "#801650", "#F46A25", "#3D3D3D", "#A285D1"];
const quotaInputs = Inputs.checkbox(Object.keys(stringToCodeMap), {value: [Object.keys(stringToCodeMap)[5]]});
const quotaSelection = Generators.input(quotaInputs);

const displayLinesInput = Inputs.checkbox(['Show dates'], {value:['Show dates']});
const displayLinesSelection = Generators.input(displayLinesInput);

const balanceHistory = await FileAttachment("./data/quota-balance-history.json").json({typed: true})
let tableData = []
for (let balanceSet in balanceHistory){
    tableData.push(balanceHistory[balanceSet].map((row) => {
      return {
        'quota__order_number':row.quota__order_number,
        'date': Date.parse(row.quota_definition__last_allocation_date),
        'percentage_remaining': (1-row.quota_definition__fill_rate)*100,
        'quota_start_date':Date.parse(row.quota_definition__validity_start_date),
        'readable_desc':row.readable_desc,
      }
    }))
}
```

```js
let plots = quotaSelection.map((string, index) => {
  let chosenIndex = tableData.findIndex((item) => item[0].readable_desc==string)
  return [Plot.dot(tableData[chosenIndex], {x: "date", y: "percentage_remaining",stroke: "readable_desc", symbol:'asterisk'}),
  tableData[chosenIndex].map((item,index) => {if (index % 10 == 0 && displayLinesSelection[0]=='Show dates') return [ Plot.ruleX({length: 500}, {x:item['quota_start_date'], strokeOpacity: 0.2})]}),]} 
) 

const marks =  [Plot.gridY(),Plot.ruleY([0], {stroke: "currentColor"}),
      Plot.ruleX(['2022-01-01'], {stroke: "currentColor"}),]

const currentVolumes = FileAttachment("./data/quotas-including-current-volumes.csv")
  .csv({typed: true})
  .then(data => data.map(row => ({
    ...row,
    // Shorten the really long geographical area names
    quota__geographical_areas: row.quota__geographical_areas.replace(/.*(.\[\d+\]).*/, 'Areas subject to category $1 safeguards')
  })));
const currentOpenCriticalVolumes = currentVolumes
  .then(data => data.filter(row => ['Open', 'Critical'].includes(row.quota_definition__status)));

function balanceHistoryChart(data, {width}) {
  return Plot.plot({
    title: "Percentage of quota remaining over time",
    subtitle: "How the percentage remaining has changed since the start of 2020 for six quotas. Data is available only at inconsistent intervals.",
    width,
    style: "font-size: 12px;",
    marginBottom: 40,
    marginTop: 30,
    x: {type: "utc", label: "Date of allocation", labelOffset: 40},
    y: {domain: [0, 100], label: "Percentage remaining"},
    color: {range:govuk_colour_palette, legend: true},
    marks: [ 
    marks,
      plots,
    ]
  })
}

function remainingChart(data, {width}) {
  return Plot.plot({
    title: "Areas with highest percentage of unused quotas",
    subtitle: "The 20 geographical areas that have the highest percentage remaining balance of open and critical quotas.",
    width,
    height: 550,
    style: "font-size: 12px;",
    marginBottom: 40,
    x: {grid: true, label: "Percentage remaining", domain: [0, 100], labelOffset: 40},
    y: {label: null},
    marks: [
      Plot.rectX(data, Plot.groupY(
        {x: (values, b) => {
          return Math.max(0, 1 - values.map(row => row.quota_definition__balance).reduce((partialSum, a) => partialSum + a, 0) / values.map(row => row.quota_definition__initial_volume).reduce((partialSum, a) => partialSum + a, 0)) * 100
        }},
        {y: "quota__geographical_areas", tip: true, sort: {y: "-x", limit: 20}, fill: govuk_colour_palette[0]}
      )),
      Plot.ruleX([0]),
      Plot.axisY({label: null, marginLeft: 300}),
    ]
  });
}
```

<div class="govuk-width-container">
  <h1 class="govuk-heading-l govuk-!-margin-top-7">Quota balances</h1>
  <div class="grid grid-cols-4">
    <div class="card">
      <h2>Open quotas 🟩</h2>
      <span class="big">${currentVolumes.filter((d) => d.quota_definition__status === "Open").length.toLocaleString("en-GB")}</span>
    </div>
    <div class="card">
      <h2>Critical quotas 🟨</h2>
      <span class="big">${currentVolumes.filter((d) => d.quota_definition__status === "Critical").length.toLocaleString("en-GB")}</span>
    </div>
    <div class="card">
      <h2>Closed quotas 🟦</h2>
      <span class="big">${currentVolumes.filter((d) => d.quota_definition__status === "Closed").length.toLocaleString("en-GB")}</span>
    </div>
    <div class="card">
      <h2>Exhausted quotas 🟥</h2>
      <span class="big">${currentVolumes.filter((d) => d.quota_definition__status === "Exhausted").length.toLocaleString("en-GB")}</span>
    </div>
  </div>
  <!-- -->
  <div class="govuk-grid-row">
    <div class="govuk-grid-column-two-thirds">
      <div class="card">
        ${resize((width) => balanceHistoryChart(balanceHistory, {width}))}
      </div>
    </div>
    <div class="govuk-grid-column-one-third">
      <div class="card height-526">
        <h2 class="govuk-heading-l govuk-!-margin-top-0 govuk-!-margin-bottom-2">Quotas to visualise:</h2>
        ${quotaInputs}
        <!-- -->
        <h2 class="govuk-heading-l govuk-!-margin-top-3 govuk-!-margin-bottom-2">Display quota renewal dates?</h2>
        ${displayLinesInput}
      </div>
    </div>
  <!-- -->
  </div>
  <div class="govuk-grid-row">
    <div class="govuk-grid-column-full">
      <h1 class="govuk-heading-l govuk-!-margin-top-7">Unused Quotas</h1>
      <div class="grid grid-cols-1">
        <div class="card">
          ${resize((width) => remainingChart(currentOpenCriticalVolumes, {width}))}
        </div>
      </div>
    </div>
  </div>
<!-- Closes .govuk-width-container -->
</div>
