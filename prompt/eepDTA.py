GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["drug", "disease", "treatment", "gene", "target", "effectiveness"]

PROMPTS["entity_extraction"] = """-Goal-
In a task named Drug-Target Analysis (Map the genes and pathways targeted by [specific drug]. Explain how these targets are implicated in [specific disease] and assess whether the drug’s mechanism of action aligns with the disease’s underlying biology.).
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
A novel compound, identified as NTR-194, demonstrates potent antiviral properties against Hepatitis C.
This drug's mechanism of action involves inhibition of the NS5A protein, a critical component for viral replication. 
Early-stage clinical trials reveal that NTR-194 significantly reduces viral load when used in combination with existing antiviral therapies, highlighting its potential to improve the overall effectiveness of the Hepatitis C treatment regimen. As we advance to later phases of clinical testing, 
detailed pharmacokinetic and pharmacodynamic profiling will be crucial to understanding its full therapeutic potential and safety profile.
################
Output:
("entity"{tuple_delimiter}"NTR-194"{tuple_delimiter}"Compound"{tuple_delimiter}"A novel compound with potent antiviral properties targeting Hepatitis C by inhibiting the NS5A protein, which is crucial for viral replication."){record_delimiter}
("entity"{tuple_delimiter}"Hepatitis C"{tuple_delimiter}"Disease"{tuple_delimiter}"A viral infection that damages the liver and can cause severe complications if untreated."){record_delimiter}
("entity"{tuple_delimiter}"NS5A protein"{tuple_delimiter}"Protein"{tuple_delimiter}"A vital component of the Hepatitis C virus necessary for its replication, targeted by NTR-194."){record_delimiter}
("entity"{tuple_delimiter}"Viral replication"{tuple_delimiter}"Biological process"{tuple_delimiter}"The process by which the Hepatitis C virus reproduces itself within host cells."){record_delimiter}
("entity"{tuple_delimiter}"Early-stage clinical trials"{tuple_delimiter}"Research process"{tuple_delimiter}"Initial phases of clinical research designed to evaluate the safety and efficacy of NTR-194 in humans."){record_delimiter}
("entity"{tuple_delimiter}"Antiviral therapies"{tuple_delimiter}"Treatment"{tuple_delimiter}"Existing treatments for viral infections, including those for Hepatitis C, used in combination with NTR-194."){record_delimiter}
("entity"{tuple_delimiter}"Pharmacokinetic profiling"{tuple_delimiter}"Scientific process"{tuple_delimiter}"The study of how a drug is absorbed, distributed, metabolized, and excreted in the body."){record_delimiter}
("entity"{tuple_delimiter}"Pharmacodynamic profiling"{tuple_delimiter}"Scientific process"{tuple_delimiter}"The study of the biochemical and physiological effects of a drug and its mechanisms of action."){record_delimiter}
("entity"{tuple_delimiter}"Hepatitis C treatment regimen"{tuple_delimiter}"Medical approach"{tuple_delimiter}"A structured plan combining various therapies to effectively manage and treat Hepatitis C."){record_delimiter}
("entity"{tuple_delimiter}"Viral load"{tuple_delimiter}"Measurement"{tuple_delimiter}"The amount of Hepatitis C virus present in a patient's bloodstream, reduced significantly by NTR-194."){record_delimiter}
("relationship"{tuple_delimiter}"NTR-194"{tuple_delimiter}"NS5A protein"{tuple_delimiter}"NTR-194 inhibits the NS5A protein to prevent viral replication of Hepatitis C."{tuple_delimiter}"inhibition, targeting"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"NTR-194"{tuple_delimiter}"Hepatitis C"{tuple_delimiter}"NTR-194 demonstrates potent antiviral properties against Hepatitis C."{tuple_delimiter}"treatment, antiviral"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"NTR-194"{tuple_delimiter}"Antiviral therapies"{tuple_delimiter}"NTR-194 enhances the effectiveness of Hepatitis C treatment when used with existing antiviral therapies."{tuple_delimiter}"combination, enhancement"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"NTR-194"{tuple_delimiter}"Viral load"{tuple_delimiter}"NTR-194 significantly reduces viral load in patients with Hepatitis C."{tuple_delimiter}"reduction, efficacy"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"Pharmacokinetic profiling"{tuple_delimiter}"NTR-194"{tuple_delimiter}"Pharmacokinetic profiling is critical to understanding the absorption and metabolism of NTR-194."{tuple_delimiter}"characterization, drug behavior"{tuple_delimiter}0.8){record_delimiter}
("relationship"{tuple_delimiter}"Pharmacodynamic profiling"{tuple_delimiter}"NTR-194"{tuple_delimiter}"Pharmacodynamic profiling will help evaluate the therapeutic effects of NTR-194."{tuple_delimiter}"evaluation, therapeutic action"{tuple_delimiter}0.8){record_delimiter}
("relationship"{tuple_delimiter}"Hepatitis C treatment regimen"{tuple_delimiter}"NTR-194"{tuple_delimiter}"NTR-194 has potential to improve the overall Hepatitis C treatment regimen."{tuple_delimiter}"improvement, therapeutic strategy"{tuple_delimiter}0.85){record_delimiter}
("content_keywords"{tuple_delimiter}"NTR-194, Hepatitis C, NS5A protein, viral replication, antiviral therapies, pharmacokinetics, pharmacodynamics, treatment regimen"){completion_delimiter}
#############################""",
    """Example 2:

Entity_types: ["drug", "disease", "treatment", "gene", "target", "effectiveness"]
Text:
The emergence of drug-resistant strains of  *Mycobacterium tuberculosis* poses a significant threat to global health. 
Traditional antibiotic treatments are increasingly ineffective against these strains, necessitating the development of novel therapeutic strategies. 
One promising approach involves targeting the MmpL3 gene, which plays a crucial role in the biosynthesis of the mycobacterial cell wall.  Drugs targeting MmpL3 have shown promising effectiveness in preclinical studies, inhibiting bacterial growth and reducing disease severity. Further research is needed to assess the long-term effectiveness and safety of these drugs in clinical settings and to determine their potential 
for combination therapy with existing anti-tuberculosis treatments.
#############
Output:
("entity"{tuple_delimiter}"Mycobacterium tuberculosis"{tuple_delimiter}"Bacterium"{tuple_delimiter}"The causative agent of tuberculosis, with emerging drug-resistant strains posing a significant global health challenge."){record_delimiter}
("entity"{tuple_delimiter}"Drug-resistant strains"{tuple_delimiter}"Pathogen characteristic"{tuple_delimiter}"Strains of Mycobacterium tuberculosis that are resistant to traditional antibiotic treatments, necessitating alternative therapeutic approaches."){record_delimiter}
("entity"{tuple_delimiter}"Antibiotic treatments"{tuple_delimiter}"Therapeutic approach"{tuple_delimiter}"Traditional treatments for tuberculosis, increasingly ineffective against drug-resistant strains."){record_delimiter}
("entity"{tuple_delimiter}"MmpL3 gene"{tuple_delimiter}"Gene"{tuple_delimiter}"A gene essential for the biosynthesis of the mycobacterial cell wall, targeted by novel drugs to inhibit bacterial growth."){record_delimiter}
("entity"{tuple_delimiter}"Novel therapeutic strategies"{tuple_delimiter}"Research process"{tuple_delimiter}"Innovative approaches aimed at combating drug-resistant Mycobacterium tuberculosis, including targeting the MmpL3 gene."){record_delimiter}
("entity"{tuple_delimiter}"Preclinical studies"{tuple_delimiter}"Research process"{tuple_delimiter}"Experimental studies evaluating the effectiveness of drugs targeting the MmpL3 gene in inhibiting bacterial growth and reducing disease severity."){record_delimiter}
("entity"{tuple_delimiter}"Clinical settings"{tuple_delimiter}"Research process"{tuple_delimiter}"The stage of research focusing on assessing the safety and efficacy of novel drugs in human patients."){record_delimiter}
("entity"{tuple_delimiter}"Combination therapy"{tuple_delimiter}"Therapeutic approach"{tuple_delimiter}"A treatment strategy that combines novel drugs targeting the MmpL3 gene with existing anti-tuberculosis treatments."){record_delimiter}
("relationship"{tuple_delimiter}"Mycobacterium tuberculosis"{tuple_delimiter}"Drug-resistant strains"{tuple_delimiter}"Drug-resistant strains of Mycobacterium tuberculosis pose a major challenge to global health and traditional antibiotic treatments."{tuple_delimiter}"resistance, health threat"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"Drug-resistant strains"{tuple_delimiter}"Antibiotic treatments"{tuple_delimiter}"Traditional antibiotic treatments are increasingly ineffective against drug-resistant strains of Mycobacterium tuberculosis."{tuple_delimiter}"ineffectiveness, resistance"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"MmpL3 gene"{tuple_delimiter}"Mycobacterium tuberculosis"{tuple_delimiter}"The MmpL3 gene plays a crucial role in the biosynthesis of the mycobacterial cell wall."{tuple_delimiter}"biosynthesis, gene function"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"Novel therapeutic strategies"{tuple_delimiter}"MmpL3 gene"{tuple_delimiter}"Targeting the MmpL3 gene is a promising novel therapeutic strategy to combat drug-resistant Mycobacterium tuberculosis."{tuple_delimiter}"targeting, innovation"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"Preclinical studies"{tuple_delimiter}"MmpL3 gene"{tuple_delimiter}"Preclinical studies have shown the effectiveness of targeting the MmpL3 gene in reducing bacterial growth."{tuple_delimiter}"evaluation, experimental success"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"Preclinical studies"{tuple_delimiter}"Clinical settings"{tuple_delimiter}"Preclinical studies provide the foundation for assessing the safety and efficacy of novel drugs in clinical settings."{tuple_delimiter}"progression, research validation"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"Combination therapy"{tuple_delimiter}"MmpL3 gene"{tuple_delimiter}"Combining drugs targeting the MmpL3 gene with existing treatments may enhance therapeutic outcomes against tuberculosis."{tuple_delimiter}"synergy, optimization"{tuple_delimiter}0.85){record_delimiter}
("content_keywords"{tuple_delimiter}"Mycobacterium tuberculosis, drug-resistant strains, MmpL3 gene, novel therapeutic strategies, preclinical studies, clinical settings, combination therapy, antibiotic resistance"){completion_delimiter}
#############################""",
    """Example 3:

Entity_types: ["drug", "disease", "treatment", "gene", "target", "effectiveness"]
Text:
Our investigation into ALK-positive non-small cell lung cancer revealed that second-generation TKI treatments demonstrated superior effectiveness compared to traditional chemotherapy. 
The presence of EML4-ALK fusion genes strongly correlated with treatment response, with progression-free survival extending to 18.9 months in the treatment group. Target engagement studies confirmed sustained inhibition of ALK phosphorylation, 
resulting in downstream pathway suppression and improved disease control.
#############
Output:
("entity"{tuple_delimiter}"ALK-positive non-small cell lung cancer"{tuple_delimiter}"Disease"{tuple_delimiter}"A subtype of lung cancer characterized by the presence of ALK mutations, which can be targeted with specific therapies."){record_delimiter}
("entity"{tuple_delimiter}"Second-generation TKI treatments"{tuple_delimiter}"Drug class"{tuple_delimiter}"A class of tyrosine kinase inhibitors that are more effective than traditional chemotherapy in treating ALK-positive non-small cell lung cancer."){record_delimiter}
("entity"{tuple_delimiter}"Traditional chemotherapy"{tuple_delimiter}"Drug class"{tuple_delimiter}"Conventional cancer treatments that have lower effectiveness in treating ALK-positive non-small cell lung cancer compared to second-generation TKIs."){record_delimiter}
("entity"{tuple_delimiter}"EML4-ALK fusion genes"{tuple_delimiter}"Genetic mutation"{tuple_delimiter}"A genetic alteration in which the EML4 gene fuses with the ALK gene, commonly found in ALK-positive non-small cell lung cancer and linked to treatment response."){record_delimiter}
("entity"{tuple_delimiter}"Progression-free survival"{tuple_delimiter}"Clinical metric"{tuple_delimiter}"A measure of the time during and after treatment in which the disease does not worsen, with an 18.9-month extension in the treatment group."){record_delimiter}
("entity"{tuple_delimiter}"ALK phosphorylation"{tuple_delimiter}"Biological process"{tuple_delimiter}"The process by which ALK is activated, which is inhibited by second-generation TKIs, leading to the suppression of downstream pathways."){record_delimiter}
("entity"{tuple_delimiter}"Downstream pathway suppression"{tuple_delimiter}"Biological process"{tuple_delimiter}"The reduction in activity of signaling pathways that are critical for tumor progression, a result of inhibiting ALK phosphorylation."){record_delimiter}
("entity"{tuple_delimiter}"Disease control"{tuple_delimiter}"Clinical outcome"{tuple_delimiter}"The ability to prevent disease progression, enhanced by second-generation TKI treatments in ALK-positive non-small cell lung cancer."){record_delimiter}
("relationship"{tuple_delimiter}"Second-generation TKI treatments"{tuple_delimiter}"Traditional chemotherapy"{tuple_delimiter}"Second-generation TKI treatments demonstrated superior effectiveness compared to traditional chemotherapy in treating ALK-positive non-small cell lung cancer."{tuple_delimiter}"effectiveness, comparison"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"ALK-positive non-small cell lung cancer"{tuple_delimiter}"Second-generation TKI treatments"{tuple_delimiter}"Second-generation TKI treatments are used to target ALK mutations in ALK-positive non-small cell lung cancer, offering superior treatment outcomes."{tuple_delimiter}"targeted treatment, efficacy"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"EML4-ALK fusion genes"{tuple_delimiter}"Second-generation TKI treatments"{tuple_delimiter}"The presence of EML4-ALK fusion genes strongly correlates with a better response to second-generation TKI treatments."{tuple_delimiter}"biomarker, treatment response"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"Progression-free survival"{tuple_delimiter}"Second-generation TKI treatments"{tuple_delimiter}"Progression-free survival extended to 18.9 months in patients treated with second-generation TKIs."{tuple_delimiter}"treatment outcome, efficacy"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"ALK phosphorylation"{tuple_delimiter}"Second-generation TKI treatments"{tuple_delimiter}"Second-generation TKI treatments effectively inhibit ALK phosphorylation, leading to suppression of downstream pathways."{tuple_delimiter}"inhibition, treatment mechanism"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"Downstream pathway suppression"{tuple_delimiter}"Disease control"{tuple_delimiter}"Downstream pathway suppression contributes to improved disease control in patients treated with second-generation TKIs."{tuple_delimiter}"mechanism, outcome"{tuple_delimiter}0.85){record_delimiter}
("content_keywords"{tuple_delimiter}"ALK-positive non-small cell lung cancer, second-generation TKI treatments, traditional chemotherapy, EML4-ALK fusion genes, progression-free survival, ALK phosphorylation, downstream pathway suppression, disease control"){completion_delimiter}
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
