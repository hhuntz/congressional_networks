# congressional_networks

The data and code here support the analysis found in [this paper](https://docs.google.com/document/d/1iXyDKIBOpaelFscCOGf-xeRlMRTJyJH_sEfQApfYgP4/edit?usp=sharing), in which bill cosponsorship relationships in the US Congress are cast as an interconnected network. See the PDF poster (in this repo) for highlights. 

Bill cosponsorship is one way in which members of Congress communicate with each other and various political operatives, with their constituents and the public more broadly, and with donors or prospective donors to their campaigns. Proposing or cosponsoring a proposed bill is a way of taking responsibility for the ideas therein; hence, cosponsorship signals political or ideological alignment, or at least collaboration, on the relevant issues in a bill. This report casts these connections between members as a network in which nodes represent members and the edges between them are weighted according to the frequency of cosponsorship. This network is then analyzed by standard quantitative network measures of each node, e.g., variations of connectedness and centrality, as well as by bipartisanship score, a new measure of how connected the member is outside of their own political party. This network data, aggregated at the member level, is then connected to other political and demographic information about each member; thus, these network and cosponsorship measures can be compared across political and demographic groups of members.

The <em>compile_data.py</em> file here expects you to have 2 data sources in a subdirectory called 'data'

1. bill data in XML files via https://github.com/unitedstates/congressor from propublica @ https://www.propublica.org/datastore/dataset/congressional-data-bulk-legislation-bills
2. data on Members of Congress from https://bioguide.congress.gov/search (download link in top right) -- this is included in the repo above

You can uncomment code in main() to save more files along the way; otherwise, this file outputs 2 files that are used in the analysis notebook:

1. edges.csv, with rows as edges and weights between id nums for MOCs w/ weights as # of cosponsorships
2. moc_info.json, which contains info on each MOC by bioguide_id

You can also skip the rest of this work and go straight to the file I used for analysis and visualization, which is in the <em>data</em> folder here and called MOC_features.csv. This is member-level data where each MOC has personal,political, and demographic information as well as scores for network measures such as pagerank and the bipartisan cosponsorship score mentioned above. 
