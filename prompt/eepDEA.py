GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["drug", "disease", "treatment", "gene", "target", "effectiveness"]

PROMPTS["entity_extraction"] = """-Goal-
In a task named Drug Effectiveness Assessment (Evaluate the effectiveness of [specific drug] for treating [specific disease]. Include an analysis of clinical or preclinical data, the strength of the drug’s interaction with its target genes or pathways, and any evidence of therapeutic outcomes.).
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
The CRISPR-Cas9 gene-editing technology has revolutionized the approach to hereditary diseases. 
By precisely modifying the defective segments within the dystrophin gene, researchers have achieved significant improvements in the effectiveness of muscular dystrophy treatments. This gene-targeted intervention has not only halted the progression of muscle degradation but also shown potential for restoring partial muscular function. 
Future investigations will focus on optimizing delivery methods and minimizing off-target effects to enhance therapeutic outcomes.
################
Output:
("entity"{tuple_delimiter}"CRISPR-Cas9"{tuple_delimiter}"Gene-editing technology"{tuple_delimiter}"A revolutionary technology for precisely modifying genes, used to treat hereditary diseases."){record_delimiter}
("entity"{tuple_delimiter}"Hereditary diseases"{tuple_delimiter}"Disease category"{tuple_delimiter}"Diseases caused by genetic defects passed from one generation to another."){record_delimiter}
("entity"{tuple_delimiter}"Dystrophin gene"{tuple_delimiter}"Gene"{tuple_delimiter}"A gene associated with muscular dystrophy, where defects lead to muscle degradation."){record_delimiter}
("entity"{tuple_delimiter}"Muscular dystrophy"{tuple_delimiter}"Disease"{tuple_delimiter}"A group of genetic diseases characterized by progressive muscle weakness and degeneration."){record_delimiter}
("entity"{tuple_delimiter}"Gene-targeted intervention"{tuple_delimiter}"Therapeutic approach"{tuple_delimiter}"A treatment strategy that focuses on modifying specific defective genes to address disease progression."){record_delimiter}
("entity"{tuple_delimiter}"Muscle degradation"{tuple_delimiter}"Biological process"{tuple_delimiter}"The progressive loss of muscle tissue and function."){record_delimiter}
("entity"{tuple_delimiter}"Partial muscular function"{tuple_delimiter}"Biological outcome"{tuple_delimiter}"The restoration of some level of muscle activity and strength."){record_delimiter}
("entity"{tuple_delimiter}"Delivery methods"{tuple_delimiter}"Process"{tuple_delimiter}"Techniques for delivering gene-editing tools to target cells or tissues effectively."){record_delimiter}
("entity"{tuple_delimiter}"Off-target effects"{tuple_delimiter}"Side effect"{tuple_delimiter}"Unintended genetic modifications caused by gene-editing technologies."){record_delimiter}
("entity"{tuple_delimiter}"Therapeutic outcomes"{tuple_delimiter}"Medical goal"{tuple_delimiter}"The results of treatment aimed at improving a patient's condition."){record_delimiter}
("relationship"{tuple_delimiter}"CRISPR-Cas9"{tuple_delimiter}"Dystrophin gene"{tuple_delimiter}"CRISPR-Cas9 modifies defective segments of the dystrophin gene to treat muscular dystrophy."{tuple_delimiter}"gene-editing, targeting"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"CRISPR-Cas9"{tuple_delimiter}"Muscular dystrophy"{tuple_delimiter}"CRISPR-Cas9 revolutionized treatment by addressing genetic defects causing muscular dystrophy."{tuple_delimiter}"treatment, innovation"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"Dystrophin gene"{tuple_delimiter}"Muscular dystrophy"{tuple_delimiter}"Defects in the dystrophin gene are a primary cause of muscular dystrophy."{tuple_delimiter}"pathology, causation"{tuple_delimiter}0.95){record_delimiter}
("relationship"{tuple_delimiter}"Gene-targeted intervention"{tuple_delimiter}"Muscle degradation"{tuple_delimiter}"Gene-targeted intervention halts muscle degradation by addressing the genetic root cause."{tuple_delimiter}"intervention, prevention"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"Gene-targeted intervention"{tuple_delimiter}"Partial muscular function"{tuple_delimiter}"Gene-targeted intervention shows potential for restoring partial muscular function."{tuple_delimiter}"restoration, treatment"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"Delivery methods"{tuple_delimiter}"CRISPR-Cas9"{tuple_delimiter}"Optimizing delivery methods is critical to enhancing CRISPR-Cas9's effectiveness."{tuple_delimiter}"optimization, delivery"{tuple_delimiter}0.8){record_delimiter}
("relationship"{tuple_delimiter}"Off-target effects"{tuple_delimiter}"CRISPR-Cas9"{tuple_delimiter}"Minimizing off-target effects is essential for safer CRISPR-Cas9 applications."{tuple_delimiter}"safety, precision"{tuple_delimiter}0.85){record_delimiter}
("content_keywords"{tuple_delimiter}"CRISPR-Cas9, hereditary diseases, dystrophin gene, muscular dystrophy, gene-targeted intervention, delivery methods, off-target effects, therapeutic outcomes"){completion_delimiter}
#############################""",
    """Example 2:

Entity_types: ["drug", "disease", "treatment", "gene", "target", "effectiveness"]
Text:
Recent advancements in CRISPR-Cas9 technology have opened up new possibilities for targeted gene therapy in the treatment of cystic fibrosis.  
The CFTR gene, commonly mutated in cystic fibrosis patients, is a prime target for this approach.
Early studies suggest a high level of effectiveness in correcting the defective CFTR gene in vitro. 
However, challenges remain in translating this in vitro effectiveness to in vivo models and ultimately to clinical trials.  Issues such as delivery efficiency to the target cells in the lungs and potential off-target effects need to be 
addressed before CRISPR-based therapies can be considered a viable treatment option for cystic fibrosis.
#############
Output:
("entity"{tuple_delimiter}"CRISPR-Cas9 technology"{tuple_delimiter}"Technology"{tuple_delimiter}"A cutting-edge gene-editing tool enabling precise modifications in DNA, used for targeted gene therapy applications."){record_delimiter}
("entity"{tuple_delimiter}"Cystic fibrosis"{tuple_delimiter}"Disease"{tuple_delimiter}"A genetic disorder that affects the lungs and other organs, caused by mutations in the CFTR gene."){record_delimiter}
("entity"{tuple_delimiter}"CFTR gene"{tuple_delimiter}"Gene"{tuple_delimiter}"The gene commonly mutated in cystic fibrosis patients, responsible for producing a protein that regulates salt and water movement in cells."){record_delimiter}
("entity"{tuple_delimiter}"Targeted gene therapy"{tuple_delimiter}"Therapeutic approach"{tuple_delimiter}"A treatment strategy that focuses on correcting or modifying specific genetic defects, such as mutations in the CFTR gene."){record_delimiter}
("entity"{tuple_delimiter}"In vitro studies"{tuple_delimiter}"Research process"{tuple_delimiter}"Laboratory studies conducted outside a living organism to evaluate the effectiveness of CRISPR-Cas9 in correcting CFTR gene mutations."){record_delimiter}
("entity"{tuple_delimiter}"In vivo models"{tuple_delimiter}"Research process"{tuple_delimiter}"Animal or other living models used to study the application and effectiveness of therapies like CRISPR-Cas9 in a living system."){record_delimiter}
("entity"{tuple_delimiter}"Clinical trials"{tuple_delimiter}"Research process"{tuple_delimiter}"Human studies designed to evaluate the safety and efficacy of CRISPR-based therapies for cystic fibrosis."){record_delimiter}
("entity"{tuple_delimiter}"Delivery efficiency"{tuple_delimiter}"Scientific challenge"{tuple_delimiter}"The effectiveness of transporting CRISPR components to target cells, such as lung cells in cystic fibrosis treatment."){record_delimiter}
("entity"{tuple_delimiter}"Off-target effects"{tuple_delimiter}"Scientific challenge"{tuple_delimiter}"Unintended changes in the genome caused by CRISPR-Cas9, potentially leading to unwanted side effects."){record_delimiter}
("relationship"{tuple_delimiter}"CRISPR-Cas9 technology"{tuple_delimiter}"CFTR gene"{tuple_delimiter}"CRISPR-Cas9 is used to correct mutations in the CFTR gene in cystic fibrosis patients."{tuple_delimiter}"gene editing, correction"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"CFTR gene"{tuple_delimiter}"Cystic fibrosis"{tuple_delimiter}"Mutations in the CFTR gene are the primary cause of cystic fibrosis."{tuple_delimiter}"causation, genetic basis"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"CRISPR-Cas9 technology"{tuple_delimiter}"Cystic fibrosis"{tuple_delimiter}"CRISPR-Cas9 offers a potential treatment for cystic fibrosis by targeting its genetic cause."{tuple_delimiter}"treatment, potential"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"In vitro studies"{tuple_delimiter}"CRISPR-Cas9 technology"{tuple_delimiter}"In vitro studies have shown the effectiveness of CRISPR-Cas9 in correcting CFTR gene mutations."{tuple_delimiter}"evaluation, effectiveness"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"In vitro studies"{tuple_delimiter}"In vivo models"{tuple_delimiter}"The success of in vitro studies needs to be replicated in in vivo models to validate the approach."{tuple_delimiter}"validation, translational research"{tuple_delimiter}0.8){record_delimiter}
("relationship"{tuple_delimiter}"In vivo models"{tuple_delimiter}"Clinical trials"{tuple_delimiter}"Results from in vivo models are critical for advancing CRISPR-based therapies to clinical trials."{tuple_delimiter}"progression, validation"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"Delivery efficiency"{tuple_delimiter}"CRISPR-Cas9 technology"{tuple_delimiter}"Improving delivery efficiency is essential for the effective application of CRISPR-Cas9 in treating cystic fibrosis."{tuple_delimiter}"optimization, application"{tuple_delimiter}0.8){record_delimiter}
("relationship"{tuple_delimiter}"Off-target effects"{tuple_delimiter}"CRISPR-Cas9 technology"{tuple_delimiter}"Addressing off-target effects is necessary to ensure the safety of CRISPR-based therapies."{tuple_delimiter}"safety, precision"{tuple_delimiter}0.8){record_delimiter}
("content_keywords"{tuple_delimiter}"CRISPR-Cas9, cystic fibrosis, CFTR gene, targeted gene therapy, in vitro, in vivo, clinical trials, delivery efficiency, off-target effects"){completion_delimiter}
#############################""",
    """Example 3:

Entity_types: ["drug", "disease", "treatment", "gene", "target", "effectiveness"]
Text:
In treating metastatic melanoma, the combination of BRAF inhibitors with MEK inhibitors showed remarkable disease control rates. 
Notably, patients expressing the BRAF V600E mutation displayed an overall survival benefit of 14.2 months when treated with Dabrafenib plus Trametinib. The dual targeting approach effectively reduced the tumor burden while simultaneously decreasing the incidence of drug resistance,
a common limitation in single-agent therapies.
#############
Output:
("entity"{tuple_delimiter}"Metastatic melanoma"{tuple_delimiter}"Disease"{tuple_delimiter}"An advanced form of skin cancer for which combination therapies involving BRAF and MEK inhibitors have shown remarkable disease control rates."){record_delimiter}
("entity"{tuple_delimiter}"BRAF inhibitors"{tuple_delimiter}"Drug class"{tuple_delimiter}"A class of drugs targeting the BRAF protein, particularly effective in patients with the BRAF V600E mutation."){record_delimiter}
("entity"{tuple_delimiter}"MEK inhibitors"{tuple_delimiter}"Drug class"{tuple_delimiter}"A class of drugs that target the MEK protein, used in combination with BRAF inhibitors to enhance therapeutic outcomes."){record_delimiter}
("entity"{tuple_delimiter}"BRAF V600E mutation"{tuple_delimiter}"Genetic mutation"{tuple_delimiter}"A specific mutation in the BRAF gene associated with increased responsiveness to therapies involving BRAF and MEK inhibitors."){record_delimiter}
("entity"{tuple_delimiter}"Dabrafenib"{tuple_delimiter}"Drug"{tuple_delimiter}"A BRAF inhibitor used in combination with Trametinib for treating metastatic melanoma, particularly in patients with the BRAF V600E mutation."){record_delimiter}
("entity"{tuple_delimiter}"Trametinib"{tuple_delimiter}"Drug"{tuple_delimiter}"A MEK inhibitor used in combination with Dabrafenib for metastatic melanoma treatment."){record_delimiter}
("entity"{tuple_delimiter}"Dual targeting approach"{tuple_delimiter}"Therapeutic approach"{tuple_delimiter}"A strategy combining BRAF and MEK inhibitors to reduce tumor burden and minimize drug resistance."){record_delimiter}
("entity"{tuple_delimiter}"Single-agent therapies"{tuple_delimiter}"Therapeutic approach"{tuple_delimiter}"Treatments using a single drug, often limited by the development of drug resistance."){record_delimiter}
("relationship"{tuple_delimiter}"BRAF inhibitors"{tuple_delimiter}"MEK inhibitors"{tuple_delimiter}"The combination of BRAF and MEK inhibitors has shown remarkable disease control rates in metastatic melanoma treatment."{tuple_delimiter}"combination, synergy"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"Metastatic melanoma"{tuple_delimiter}"BRAF inhibitors"{tuple_delimiter}"BRAF inhibitors are a key component in the treatment of metastatic melanoma, especially for patients with the BRAF V600E mutation."{tuple_delimiter}"treatment, targeted therapy"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"Metastatic melanoma"{tuple_delimiter}"MEK inhibitors"{tuple_delimiter}"MEK inhibitors, when combined with BRAF inhibitors, are effective in controlling metastatic melanoma."{tuple_delimiter}"treatment, combination therapy"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"BRAF V600E mutation"{tuple_delimiter}"Dabrafenib"{tuple_delimiter}"Patients with the BRAF V600E mutation benefit significantly from treatment with Dabrafenib."{tuple_delimiter}"mutation-response, targeted therapy"{tuple_delimiter}0.9){record_delimiter}
("relationship"{tuple_delimiter}"BRAF V600E mutation"{tuple_delimiter}"Trametinib"{tuple_delimiter}"The combination of Trametinib with Dabrafenib enhances treatment outcomes for patients with the BRAF V600E mutation."{tuple_delimiter}"mutation-response, synergy"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"Dual targeting approach"{tuple_delimiter}"Single-agent therapies"{tuple_delimiter}"The dual targeting approach overcomes the limitations of single-agent therapies, such as drug resistance."{tuple_delimiter}"comparison, effectiveness"{tuple_delimiter}0.85){record_delimiter}
("relationship"{tuple_delimiter}"Dual targeting approach"{tuple_delimiter}"Metastatic melanoma"{tuple_delimiter}"The dual targeting approach is an effective strategy to reduce tumor burden in metastatic melanoma."{tuple_delimiter}"strategy, efficacy"{tuple_delimiter}0.85){record_delimiter}
("content_keywords"{tuple_delimiter}"Metastatic melanoma, BRAF inhibitors, MEK inhibitors, BRAF V600E mutation, Dabrafenib, Trametinib, dual targeting approach, tumor burden, drug resistance"){completion_delimiter}
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
