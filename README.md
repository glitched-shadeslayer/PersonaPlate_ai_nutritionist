# PersonaPlate: Contextual Language Modeling for Individualised Diets

Contributors: Mansi Nanavati, Ajjkumar Patel, Shweta Pardeshi

The increasing prevalence of personalized health and wellness trends necessitates advanced approaches for tailored dietary recommendations. 
This project introduces PersonaPlate: Contextual Language Modeling for Individualised Diets, a novel framework designed to generate personalized meal plans tailored 
to individual dietary needs and preferences. We present and evaluate three distinct methods for achieving this: a multi-agent collaborative system, 
a Retrieval Augmented Generation (RAG)-based approach integrating external nutritional information, and a QLoRA fine-tuned Llama-3.2-1B Large Language Model. 
Our evaluation methodology focuses on quantitatively analyzing the macro and micro-nutrient intake of generated meal plans against the average required nutrients 
for various user profiles. Results indicate that the multi-agent collaborative system significantly outperforms other methods, followed by the RAG-based system, 
while the QLoRA fine-tuned Llama-3.2-1B model exhibited limited coherence in its outputs.

The multi-agent flow is best understood in `multi_agent_flow.py`. RAG process can be found in `RAG.ipynb`. Finetuning Llama-3.2-1B using QLoRA and the model's inference outputs are in `qlora_finetuning_pipeline.ipynb`.
The report and presentation slides are saved as `DeepGen_Final_Report.pdf` and `DeepGen_PPT.pdf` respectively.