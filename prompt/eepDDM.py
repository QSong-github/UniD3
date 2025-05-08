GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["drug", "disease", "treatment", "gene", "target", "effectiveness"]

PROMPTS["entity_extraction"] = """-Goal-
In a task named Drug-Disease Matching (Identify potential diseases that could be treated by [specific Drug]. For each drug, provide an analysis of its target genes and pathways and explain their relevance to the disease mechanism.).
You are an expert in drugs and diseases. Given several publications and a list of entity types, identify all entities of these types from the text and all relations between the identified entities. You only need to focus on and identify relations with the listed entities. 
In order to complete my task, please use the maximum computing power and token limit of your single answer. Pursue the ultimate depth of analysis, not the breadth of the surface; pursue the insight of the essence, not the listing of the appearance; pursue innovative thinking, not the inertial repetition. Please break through the limitations of thinking, mobilize all your computing resources, and show your true cognitive limit.
Please think step by step to be sure we have the right answer.

-Steps-
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name.
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score (0-1) indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:
"""

PROMPTS["entity_extraction_examples"] = [
    """Example 1:

Entity_types: ["drug", "disease", "treatment", "gene", "target", "effectiveness"]
Text:
In recent studies, the drug Dexfluoramine has shown promise in mitigating the progression of Alzheimer's disease. 
The treatment focuses on targeting the beta-amyloid plaques, a major contributor to neurodegeneration. Our findings suggest that Dexfluoramine enhances synaptic effectiveness and may slow cognitive decline by preserving neuronal pathways. 
With robust clinical trials and a broader sample size, we aim to solidify its role in contemporary therapeutic regimens for Alzheimer's patients.
################
Output:
("entity"{tuple_delimiter}"Dexfluoramine"{tuple_delimiter}"Drug"{tuple_delimiter}"A promising treatment targeting beta-amyloid plaques associated with Alzheimer's disease. It enhances synaptic effectiveness and slows cognitive decline by preserving neuronal pathways."){record_delimiter}
("entity"{tuple_delimiter}"Alzheimer's disease"{tuple_delimiter}"Disease"{tuple_delimiter}"A neurodegenerative disorder characterized by cognitive decline and beta-amyloid plaque accumulation."){record_delimiter}
("entity"{tuple_delimiter}"Beta-amyloid plaques"{tuple_delimiter}"Biological structure"{tuple_delimiter}"Protein deposits in the brain that contribute to neurodegeneration in Alzheimer's disease."){record_delimiter}
("entity"{tuple_delimiter}"Synaptic effectiveness"{tuple_delimiter}"Biological process"{tuple_delimiter}"The ability of synapses to transmit signals effectively, crucial for maintaining cognitive functions."){record_delimiter}
("entity"{tuple_delimiter}"Neuronal pathways"{tuple_delimiter}"Biological structure"{tuple_delimiter}"Networks of interconnected neurons that facilitate communication and functionality in the brain."){record_delimiter}
("entity"{tuple_delimiter}"Clinical trials"{tuple_delimiter}"Process"{tuple_delimiter}"Research studies conducted with human participants to evaluate the safety and efficacy of treatments."){record_delimiter}
("entity"{tuple_delimiter}"Therapeutic regimens"{tuple_delimiter}"Medical approach"{tuple_delimiter}"Comprehensive treatment plans designed to manage or treat diseases."){record_delimiter}
("relationship"{tuple_delimiter}"Dexfluoramine"{tuple_delimiter}"Beta-amyloid plaques"{tuple_delimiter}"Dexfluoramine targets beta-amyloid plaques to mitigate their contribution to neurodegeneration."{tuple_delimiter}"targeting, treatment"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"Dexfluoramine"{tuple_delimiter}"Synaptic effectiveness"{tuple_delimiter}"Dexfluoramine enhances synaptic effectiveness, supporting improved cognitive function."{tuple_delimiter}"enhancement, preservation"{tuple_delimiter}0.8){record_delimiter}
("relationship"{tuple_delimiter}"Dexfluoramine"{tuple_delimiter}"Neuronal pathways"{tuple_delimiter}"Dexfluoramine helps preserve neuronal pathways, which are vital for reducing cognitive decline."{tuple_delimiter}"preservation, neuroprotection"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"Dexfluoramine"{tuple_delimiter}"Alzheimer's isease"{tuple_delimiter}"Dexfluoramine shows potential in slowing the progression of Alzheimer's disease."{tuple_delimiter}"treatment, mitigation"{tuple_delimiter}0.9)
("relationship"{tuple_delimiter}"Beta-amyloid plaques"{tuple_delimiter}"Alzheimer's disease"{tuple_delimiter}"Beta-amyloid plaques are a major contributor to neurodegeneration in Alzheimer's disease."{tuple_delimiter}"contribution, pathology"{tuple_delimiter}0.95){record_delimiter}
("relationship"{tuple_delimiter}"Clinical trials"{tuple_delimiter}"Dexfluoramine"{tuple_delimiter}"Clinical trials are essential to evaluate the effectiveness of Dexfluoramine for Alzheimer's disease."{tuple_delimiter}"evaluation, validation"{tuple_delimiter}0.8){record_delimiter}
("relationship"{tuple_delimiter}"Therapeutic regimens"{tuple_delimiter}"Dexfluoramine"{tuple_delimiter}"Dexfluoramine has potential to become part of contemporary therapeutic regimens for Alzheimer's patients."{tuple_delimiter}"inclusion, strategy"{tuple_delimiter}0.85){record_delimiter}
("content_keywords"{tuple_delimiter}"Dexfluoramine, Alzheimer's disease, beta-amyloid plaques, synaptic effectiveness, cognitive decline, clinical trials, therapeutic regimens"){completion_delimiter}
#############################""",
    """Example 2:

Entity_types: ["drug", "disease", "treatment", "gene", "target", "effectiveness"]
Text:
The effectiveness of the novel drug, Xylotril, in treating Huntington's disease remains a critical area of investigation. 
While preclinical studies indicated Xylotril's ability to target the mutant HTT gene, reducing its expression and mitigating neuronal damage, 
translating this success to clinical trials has presented challenges. 
Specifically, patient stratification based on HTT gene CAG repeat length appears crucial for optimizing treatment effectiveness. 
Further investigation is warranted to determine whether Xylotril’s efficacy is enhanced in patients with specific CAG repeat lengths, thereby establishing it as a viable treatment option for this debilitating disease.
#############
Output:
("entity"{tuple_delimiter}"Xylotril"{tuple_delimiter}"Drug"{tuple_delimiter}"A novel drug investigated for treating Huntington's disease by targeting the mutant HTT gene to reduce its expression and mitigate neuronal damage."){record_delimiter}
("entity"{tuple_delimiter}"Huntington's disease"{tuple_delimiter}"Disease"{tuple_delimiter}"A genetic neurodegenerative disorder caused by mutations in the HTT gene, characterized by progressive neuronal damage and cognitive decline."){record_delimiter}
("entity"{tuple_delimiter}"HTT gene"{tuple_delimiter}"Gene"{tuple_delimiter}"The gene responsible for Huntington's disease, mutations in which, particularly CAG repeat expansions, cause the condition."){record_delimiter}
("entity"{tuple_delimiter}"CAG repeat length"{tuple_delimiter}"Genetic marker"{tuple_delimiter}"A specific sequence in the HTT gene, the length of which is associated with the severity and progression of Huntington's disease."){record_delimiter}
("entity"{tuple_delimiter}"Preclinical studies"{tuple_delimiter}"Research process"{tuple_delimiter}"Early experimental research conducted to evaluate the potential efficacy and safety of Xylotril before clinical trials."){record_delimiter}
("entity"{tuple_delimiter}"Clinical trials"{tuple_delimiter}"Research process"{tuple_delimiter}"Human studies aimed at assessing the safety, efficacy, and optimal usage of Xylotril for treating Huntington's disease."){record_delimiter}
("entity"{tuple_delimiter}"Patient stratification"{tuple_delimiter}"Clinical approach"{tuple_delimiter}"Grouping patients based on genetic or clinical characteristics, such as HTT gene CAG repeat length, to optimize treatment outcomes."){record_delimiter}
("relationship"{tuple_delimiter}"Xylotril"{tuple_delimiter}"HTT gene"{tuple_delimiter}"Xylotril targets the mutant HTT gene to reduce its expression and mitigate neuronal damage."{tuple_delimiter}"targeting, genetic modification"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"Xylotril"{tuple_delimiter}"Huntington's disease"{tuple_delimiter}"Xylotril is under investigation as a potential treatment for Huntington's disease."{tuple_delimiter}"treatment, investigation"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"HTT gene"{tuple_delimiter}"CAG repeat length"{tuple_delimiter}"The CAG repeat length in the HTT gene influences the progression and severity of Huntington's disease."{tuple_delimiter}"genetic influence, severity"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"CAG repeat length"{tuple_delimiter}"Patient stratification"{tuple_delimiter}"Stratifying patients based on HTT gene CAG repeat length may optimize treatment with Xylotril."{tuple_delimiter}"personalized medicine, optimization"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"Preclinical studies"{tuple_delimiter}"Xylotril"{tuple_delimiter}"Preclinical studies demonstrated Xylotril's ability to reduce HTT gene expression and mitigate neuronal damage."{tuple_delimiter}"efficacy, experimental research"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"Clinical trials"{tuple_delimiter}"Xylotril"{tuple_delimiter}"Clinical trials are needed to confirm Xylotril's effectiveness and safety in treating Huntington's disease."{tuple_delimiter}"validation, treatment evaluation"{tuple_delimiter}0.85){record_delimiter}
("content_keywords"{tuple_delimiter}"Xylotril, Huntington's disease, HTT gene, CAG repeat length, patient stratification, preclinical studies, clinical trials, treatment optimization"){completion_delimiter}
#############################""",
    """Example 3:

Entity_types: ["drug", "disease", "treatment", "gene", "target", "effectiveness"]
Text:
The administration of Lenvatinib demonstrated significant efficacy in targeting the FGFR signaling pathway in patients with advanced hepatocellular carcinoma. 
Our analysis revealed that patients carrying the VEGFR2 mutation exhibited a markedly improved response rate of 68%, compared to 31% in the control group. 
The treatment's effectiveness was particularly pronounced in cases where the JAK1/STAT3 pathway showed heightened activity, suggesting a potential synergistic mechanism of action.
#############
Output:
("entity"{tuple_delimiter}"Lenvatinib"{tuple_delimiter}"Drug"{tuple_delimiter}"A therapeutic agent shown to target the FGFR signaling pathway effectively in advanced hepatocellular carcinoma patients."){record_delimiter}
("entity"{tuple_delimiter}"FGFR signaling pathway"{tuple_delimiter}"Biological pathway"{tuple_delimiter}"A critical pathway involved in cellular growth and survival, targeted by Lenvatinib to treat hepatocellular carcinoma."){record_delimiter}
("entity"{tuple_delimiter}"Hepatocellular carcinoma"{tuple_delimiter}"Disease"{tuple_delimiter}"A type of liver cancer for which Lenvatinib has demonstrated significant therapeutic efficacy."){record_delimiter}
("entity"{tuple_delimiter}"VEGFR2 mutation"{tuple_delimiter}"Genetic mutation"{tuple_delimiter}"A mutation associated with a markedly improved response to Lenvatinib treatment, with a response rate of 68%."){record_delimiter}
("entity"{tuple_delimiter}"JAK1/STAT3 pathway"{tuple_delimiter}"Biological pathway"{tuple_delimiter}"A signaling pathway associated with heightened activity, contributing to the synergistic mechanism of action for Lenvatinib."){record_delimiter}
("entity"{tuple_delimiter}"Control group"{tuple_delimiter}"Research process"{tuple_delimiter}"A group of patients receiving standard care, showing a response rate of 31% compared to 68% in the VEGFR2 mutation group."){record_delimiter}
("relationship"{tuple_delimiter}"Lenvatinib"{tuple_delimiter}"FGFR signaling pathway"{tuple_delimiter}"Lenvatinib targets the FGFR signaling pathway, demonstrating efficacy in treating advanced hepatocellular carcinoma."{tuple_delimiter}"targeting, treatment"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"Lenvatinib"{tuple_delimiter}"Hepatocellular carcinoma"{tuple_delimiter}"Lenvatinib has shown significant efficacy in patients with advanced hepatocellular carcinoma."{tuple_delimiter}"treatment, efficacy"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"VEGFR2 mutation"{tuple_delimiter}"Lenvatinib"{tuple_delimiter}"Patients with the VEGFR2 mutation exhibited a markedly improved response to Lenvatinib treatment."{tuple_delimiter}"mutation-response, effectiveness"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"VEGFR2 mutation"{tuple_delimiter}"Hepatocellular carcinoma"{tuple_delimiter}"The VEGFR2 mutation is a genetic marker influencing the response rate in hepatocellular carcinoma treatment."{tuple_delimiter}"marker, response rate"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"JAK1/STAT3 pathway"{tuple_delimiter}"Lenvatinib"{tuple_delimiter}"Heightened activity in the JAK1/STAT3 pathway suggests a synergistic mechanism of action for Lenvatinib."{tuple_delimiter}"synergy, pathway activity"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"Control group"{tuple_delimiter}"VEGFR2 mutation"{tuple_delimiter}"Patients in the control group exhibited a lower response rate compared to those with the VEGFR2 mutation."{tuple_delimiter}"comparison, response rate"{tuple_delimiter}0.8){record_delimiter}
("content_keywords"{tuple_delimiter}"Lenvatinib, FGFR signaling pathway, hepatocellular carcinoma, VEGFR2 mutation, JAK1/STAT3 pathway, control group, response rate, treatment efficacy, synergy"){completion_delimiter}
#############################""",
]









PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.
Use {language} as output language.

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """MANY entities were missed in the last extraction.  Add them below using the same format:
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """It appears some entities may have still been missed.  Answer YES | NO if there are still entities that need to be added.
"""

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to questions about data in the tables provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

When handling relationships with timestamps:
1. Each relationship has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting relationships, consider both the semantic content and the timestamp
3. Don't automatically prefer the most recently created relationships - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Target response length and format---

{response_type}

---Data tables---

{context_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown."""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query.

---Goal---

Given the query, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Output the keywords in JSON format.
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes.
  - "low_level_keywords" for specific entities or details.

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "Identify potential drugs that could treat Alzheimer's disease. For each drug, provide an analysis of its target genes and pathways and explain their relevance to the disease mechanism."
################
Output:
{
  "high_level_keywords": ["Alzheimer's disease", "Potential drugs", "Target genes", "Pathways", "Disease mechanism"],
  "low_level_keywords": ["Beta-amyloid", "Tau protein", "Cholinesterase inhibitors", "NMDA receptor antagonists", "Neuroinflammation"]
}
#############################""",
    """Example 2:

Query: "Evaluate the effectiveness of Remdesivir for treating COVID-19. Include an analysis of clinical or preclinical data, the strength of the drug’s interaction with its target genes or pathways, and any evidence of therapeutic outcomes."
################
Output:
{
  "high_level_keywords": ["Remdesivir", "COVID-19", "Effectiveness", "Clinical data", "Preclinical data", "Therapeutic outcomes"],
  "low_level_keywords": ["Viral RNA polymerase inhibition", "Clinical trials", "Viral load reduction", "Survival rate", "Recovery time"]
}
#############################""",
    """Example 3:

Query: "Map the genes and pathways targeted by Trastuzumab. Explain how these targets are implicated in HER2-positive breast cancer and assess whether the drug’s mechanism of action aligns with the disease’s underlying biology."
################
Output:
{
  "high_level_keywords": ["Trastuzumab", "HER2-positive breast cancer", "Target genes", "Pathways", "Disease mechanism"],
  "low_level_keywords": ["HER2/neu receptor", "PI3K/AKT signaling pathway", "Cell proliferation", "Apoptosis", "Targeted therapy"]
}
#############################""",
]


PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to questions about documents provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

When handling content with timestamps:
1. Each piece of content has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content and the timestamp
3. Don't automatically prefer the most recent content - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Target response length and format---

{response_type}

---Documents---

{content_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""

PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate the following two points and provide a similarity score between 0 and 1 directly:
1. Whether these two questions are semantically similar
2. Whether the answer to Question 2 can be used to answer Question 1
Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""

PROMPTS["mix_rag_response"] = """---Role---

You are a professional assistant responsible for answering questions based on knowledge graph and textual information. Please respond in the same language as the user's question.

---Goal---

Generate a concise response that summarizes relevant points from the provided information. If you don't know the answer, just say so. Do not make anything up or include information where the supporting evidence is not provided.

When handling information with timestamps:
1. Each piece of information (both relationships and content) has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content/relationship and the timestamp
3. Don't automatically prefer the most recent information - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Data Sources---

1. Knowledge Graph Data:
{kg_context}

2. Vector Data:
{vector_context}

---Response Requirements---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Aim to keep content around 3 paragraphs for conciseness
- Each paragraph should be under a relevant section heading
- Each section should focus on one main point or aspect of the answer
- Use clear and descriptive section titles that reflect the content
- List up to 5 most important reference sources at the end under "References", clearly indicating whether each source is from Knowledge Graph (KG) or Vector Data (VD)
  Format: [KG/VD] Source content

Add sections and commentary to the response as appropriate for the length and format. If the provided information is insufficient to answer the question, clearly state that you don't know or cannot provide an answer in the same language as the user's question."""
