# AnalysisAiBot
Anaylsis images from short videos


demoaivison.py -> convert all image files to base64 and review

AnalysisAiBotV0.1 py -> add json template directly (but still get different format answer)

AnalysisAiBotV0.2 py  -> answer better form, but still not follow format

AnalysisAiBotV0.3 py  -> bring json contents from json files
                      -> use one-shot tech to improve the answer formatting 
                        (but the given answer format also made form gpt not human so need to be changed)
                        (and one-shot is not enough, two or three shot..)
                        Increase max token 3000 -> 4000
                        (input img max is 30~39 [predict:35])

AnalysisAiBotV0.4 py (AnaylsisAiBotStreamlit.py) -> same results,but now can change the images folder, change template, saved json file name
  streamlit run name.py