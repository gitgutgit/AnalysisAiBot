# AnalysisAiBot
(AnalysisAibot.py <- this is most recent version)
## how to excute
streamlit run AnalysisAibot.py on terminal  (need to install streamlit before running this)

## 1. MultipleimgsAi (Prompt reinforcement learning for better performance )

oldversion - imgAi.py (single img)

MultipleImgsAi_V0.1.py  ->  Multiple img

MultipleImgsAi_V0.2.py  -> write results on json,txt files , and set reasonable max_token value by variable

MultipleImgsAi_V0.3.py -> Korean version tag, increase maxtokens per each img 800 -> 1100 

MultipleImgsAi_V0.4.py -> enhance prompt (optimize + control simple case (ex: only logo) )

MultipleImgsAi_V0.5.py -> add Cost Cacluation (token calculator), fix encoding (but  answers become simple)

MultipleImgsAi_V0.6.py (second goal done) ->  imgs->textExplanation(until 0.5v) , imgs->textExplanation->Tag(0.6v~)!!

MultipleImgsAi_v0.7.py -> 1. normal python -> streamlit python
                          2. option eng,kor version (template % answer)
                          3. control bar (temperature (default =0.3)) 
(After v0.7, AnaalysisBot and MultipleImgsAi are integreted)


todolist -> 1. reduce hallucination

                          
## 2. AnalysisAibot
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



AnalysisAiBotV0.5 py (AnaylsisAiBotStreamlit.py is not 0.5v, but experiment version):
Fix the critical bugs that bring the wrong order files from path. ->  previous (lesser than 20 percent accurancy) - > near to 60 percent.

AnalysisAiBotV0.6py 
until 0.5V ,  img -> text(explanation) -> tag
0.6v   img-> tag (direct)

