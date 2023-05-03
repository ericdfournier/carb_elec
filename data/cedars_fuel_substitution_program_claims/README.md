# Data Source

https://cedars.sound-data.com/

![image info](./img/cedars.png)

# Data Overview

- TBA

# Data Description

- TBA

## Important Notes

* Raw CEDARS program claims data were preprocessed to extract fuel switching programs. This was done by matching the listed measure types in the program claim attributes to keywords that were deemed to be associated with fuel switching measures (i.e. 'heat-pump', 'gas replacement', 'panel upgrades', etc.) Extracting relevant records involved an interative process of sampling and filtering the measure type descriptions within each vintage year of claim data.
* Once relevant fuel switching program claims were extracted, additional filtering was performed on the basis of values in the 'Gross Measure Cost' attribute column. Inspection of these values revealed that there were a small number of claims, with 'Gross Measure Costs' that were either non-sensical - i.e. negative dollar amounts - or unreasonably high - i.e. greater than 1 million dollars per claim. This latter situation is illustrated in the histogram plot provided which was generated for the initial subset of fuel-substitution claims generated from the previous filtering operation. On the basis of this frequency distribution shown in this plot, the decision was taken to discard claims whose 'Gross Measure Cost' was greater than $100,000 - plotted with the broken red vertical line - as these are either likely not indicative of a 'typical' residential/small commercial fuel-switching project or are otherwise somehow aggregating multiple individual claims into one.

    <img src='./img/major_minor_threshold_hist_plot.png' width = 60%>

# Data Dictionary

- TBA
