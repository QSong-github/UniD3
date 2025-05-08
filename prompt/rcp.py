prompt4paperClass = """
You should think as an expert in the medical field, I will give you a bunch of research paper titles. Please select the appropriate papers for the three tasks I set. You need to classify each paper title. Of course, if you think a paper does not belong to any task, you can classify it as "irrelevant". The following are the specific descriptions of the three tasks:

Task1:
Drug Disease Matching
Identify potential drugs that could treat [specific disease]. For each drug, provide an analysis of its target genes and pathways and explain their relevance to the disease mechanism.

Task2:
Drug Effectiveness Assessment
Evaluate the effectiveness of [specific drug] for treating [specific disease]. Include an analysis of clinical or preclinical data, the strength of the drug's interaction with its target genes or pathways, and any evidence of therapeutic outcomes.

Task3:
Drug Target Analysis
Map the genes and pathways targeted by [specific drug]. Explain how these targets are implicated in [specific disease] and assess whether the drug's mechanism of action aligns with the disease's underlying biology.

You must give the result in the following format:
Drug Disease Matching:[title1,title2,title3,title4,...]

Drug Effectiveness Assessment:[title1,title2,title4,title4,...]

Drug Target Analysis:[title1,title2,title3,title4,...]

Now think carefully and categorize these titles carefully. 
The following are the titles that need to be categorized:

"""