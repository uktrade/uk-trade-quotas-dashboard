---
# Title is empty since this is a single page site, and the <title> element will contain the site name
title: 
toc: false
theme: air
---
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

  <div class="grid grid-cols-1">
    <div class="card">
      ${resize((width) => balanceHistoryChart(balanceHistory, {width}))}
    </div>
  </div>

  <div class="grid grid-cols-1">
    <div class="card">
      ${resize((width) => remainingChart(currentOpenCriticalVolumes, {width}))}
    </div>
  </div>

<!-- Closes .govuk-width-container -->
</div>

```js
 // Ideally use only the first 4, and in the order they appear 
let govuk_colour_palette = ["#12436D", "#28A197", "#801650", "#F46A25", "#3D3D3D", "#A285D1"]

```

<h1 class="govuk-heading-l govuk-!-margin-top-7">Quota balances ⚖️</h1>

<div class="govuk-width-container">
    <div class="govuk-grid-row">
      <div class="govuk-grid-column-two-thirds">
        <div class="card">
          ${resize((width) => balancesChart(sortedBalances, {width}))} 
          $ <!--TODO REMOVE cash sign added for visibility in html below-->
        </div> 
      </div>
      <div class="govuk-grid-column-one-third">
       <div class="card">


```js


const stringToCodeMap = {
  "Food preparation (US)":"050096",
  "Wine (ERGA OMNES)":"050097",
  "Sausages (ERGA OMNES)":"050120",
  "Fruits/Nuts (Turkey)":"050212",
  "Dried vegetables (ERGA OMNES)": "050035",
  "Pasta (Turkey)": "050232",
}

let plots = selection.map((string) =>
  [Plot.dot(sortedBalances[stringToCodeMap[string]], {x: "date", y: "percentage_remaining",stroke: "quota__order_number", symbol:'asterisk'}),
 // sortedBalances[quotaCode].map((item) => [ Plot.ruleX({length: 500}, {x:item['quota_start_date'], strokeOpacity: 0.2})]),
  Plot.ruleX({length: 500}, {x: sortedBalances[stringToCodeMap[string]][10]['quota_start_date'], strokeOpacity: 0.2})
) 

const marks =  [Plot.ruleY([0], {stroke: "currentColor"}),
      Plot.ruleX(['2022-01-01'], {stroke: "currentColor"}),]

const balanceHistory = await FileAttachment("./data/quota-balance-history.json")
  .json({typed: true})
  .then(data => data.map(row => ({
    quota__order_number: row.quota__order_number,
    date: Date.parse(row.quota_definition__last_allocation_date),
    percentage_remaining: (1-row.quota_definition__fill_rate)*100,
    'quota_start_date':Date.parse(row.quota_definition__validity_start_date),
  })));
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
    subtitle: "How the percentage remaining has changed since the start of 2020 for four quotas. Data is available only at inconsistent intervals.",
    width,
    style: "font-size: 12px;",
    marginBottom: 40,
    marginTop: 30,
    x: {type: "utc", label: "Date of allocation", labelOffset: 40},
    y: {domain: [0, 100], label: "Percentage remaining"},
    color: {range:govuk_colour_palette, legend: true},
    marks: [ // add a conditional a la: if (document.querySelector('input[type=checkbox]').checked)
    marks,
      plots,
    ]
  })
}


//viewof colors = Inputs.checkbox(["red", "green", "blue"], {label: "color"})
```


<div class="govuk-checkboxes">
      <div class="govuk-checkboxes__item">
<h2>
        Which quotas would you like to visualise?
      </h2>


```js
//const selection = view(Inputs.checkbox(["050096", "050097", "050120","050212","050035","050232"],))
const selection = view(Inputs.checkbox(["Food preparation (US)", "Wine (ERGA OMNES)", "Sausages (ERGA OMNES)","Fruits/Nuts (Turkey)","Dried vegetables (ERGA OMNES)","Pasta (Turkey)"],))
```

</div>
</div>

<div class="govuk-checkboxes" data-module="govuk-checkboxes">
      <div class="govuk-checkboxes__item">
        <input class="govuk-checkboxes__input" id="waste" name="waste" type="checkbox" value="carcasses">
        <label class="govuk-label govuk-checkboxes__label" for="waste">
          Govuk style
        </label>
      </div>
      </div>



</div>
      </div>
      </div>
    </div>
</div>
<div class="govuk-width-container">
<h1 class="govuk-heading-l govuk-!-margin-top-7">Unused Quotas</h1>

```js
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
