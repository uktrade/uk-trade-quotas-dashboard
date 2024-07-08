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
        'quota_start_date':Date.parse(row.quota_definition__validity_start_date),
      }
    }))
}
```
<div class="govuk-width-container">

```js
let govuk_colour_palette = ["#12436D", "#28A197", "#801650", "#F46A25", "#3D3D3D", "#A285D1"] // Ideally use only the first 4, and in the order they appear 

let sortedBalances={}

for (let i=0;i < tableData.length;i++){
  sortedBalances[tableData[i][0].id]=(tableData[i].toSorted(function(a,b) {
    return b['date'] - a['date']
}));
}

//let enabledBalances=[]
//if (document.querySelector('#checkbox_050097').checked){
 // enabledBalances.push(sortedBalances['050097'])
 // console.log(enabledBalances)
//} else {
//  enabledBalances = enabledBalances.filter(function( obj ) {
 //   return obj.id !== '050097';
 //   console.log(enabledBalances)
//})
//}






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
  [Plot.dot(sortedBalances[stringToCodeMap[string]], {x: "date", y: "percentage_remaining",stroke: "id", symbol:'asterisk'}),
 // sortedBalances[quotaCode].map((item) => [ Plot.ruleX({length: 500}, {x:item['quota_start_date'], strokeOpacity: 0.2})]),
  Plot.ruleX({length: 500}, {x: sortedBalances[stringToCodeMap[string]][10]['quota_start_date'], strokeOpacity: 0.2})
]
) 

const marks = [Plot.gridX(),Plot.gridY()]

function balancesChart(data, {width}) {
  return Plot.plot({
    title: "Percentage of quota remaining over time",
    width,
    x: {type: "utc"},
    y: {domain: [0, 100]},
    color: {range:govuk_colour_palette,legend: true},
    marks: [ // add a conditional a la: if (document.querySelector('input[type=checkbox]').checked)
    Plot.gridX(),Plot.gridY(),
      plots
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

<!-- Closes .govuk-width-container -->
</div>
