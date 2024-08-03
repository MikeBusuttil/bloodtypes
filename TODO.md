# TODO

## MVP
- verify the sizes match prevalence
- auto-publish with github action
- pick better colors (with + complimenting -)

### extras

- don't transfer data with every hover change (only the ones that matter)
  - egress bandwidth is gonna be nuts
  - instead use client-side callbacks: https://dash.plotly.com/clientside-callbacks
- allow showing just 1 blood type at a time by selecting from a drop-down
  - should play nicely with the hover selectability

## use non-plotly tool
- improve distinguishibility by centering and making adjacent visible links
- get everything visible at once
- color the links using gradient from source to sink
- position labels ([maybe plotly isn't the best tool](https://stackoverflow.com/questions/65012892/how-to-specify-node-label-position-for-sankey-diagram-in-plotly))
- show percentage labels:
  - % of population in center of each item in center color
  - % of population included & excluded for each side of center

- somehow represent how valuable some of the rarer blood types are
- visualize with a tree/graph to highlight the Interconnectedness (& lack thereof) of some of the types
- show 200 people icons of different color (blood type) and by clicking on each 1 you see who they can get from & give to
- source prevalence data for different countries (&/or collections of countries or regions)
