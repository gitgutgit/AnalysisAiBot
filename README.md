# AnalysisAiBot

[Quick start]
 [Setting]
 1. pip install -r requirements.txt  <-install packages 
AnalysisAibot.py <- this is most recent version
main.py <- fast api

 2/ Default directory structure for  application (the paths can be changed during the app execution process):

  3/ Need to generate  api_secrets.toml file put api key, and image_sample folder in documents, if you use default directory
```plaintext
your_folder/
├── main.py
├── api_secrets.toml
├── templates/
│   └── index.html
├── documents/
│   └── image_sample
│       └── Images1
│           ├── video_F001.png
│           └── .... (other image files)
│   └── json/
│       ├── visual_tag_en.json
│       ├── visual_tag_kor.json
│       ├── response_sample_en.json
│       ├── response_sample_kor.json
└── results/ 

```
## how to excute

[Sstreamlit version] streamlit run AnalysisAibot.py on terminal  (need to install streamlit before running this) 

[FastApi version] uvicorn main:app --reload --port 8000  (8000 is port number)   

                    ->  http://127.0.0.1:8000/docs     (8000 is port number)
                  

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


todolist -> 1. reduce hallucination (Find optimal temperature & enhance prompt)
                          
## 2. AnalysisAibot
Anaylsis images from short videos


demoaivison.py -> convert all image files to base64 and review

AnalysisAiBot_V0.1.py -> add json template directly (but still get different format answer)

AnalysisAiBot_V0.2.py  -> answer better form, but still not follow format

AnalysisAiBot_V0.3.py  -> bring json contents from json files
                      -> use one-shot tech to improve the answer formatting 
                        (but the given answer format also made form gpt not human so need to be changed)
                        (and one-shot is not enough, two or three shot..)
                        Increase max token 3000 -> 4000
                        (input img max is 30~39 [predict:35])

AnalysisAiBot_V0.4.py (AnaylsisAiBotStreamlit.py) -> same results,but now can change the images folder, change template, saved json file name
  streamlit run name.py



AnalysisAiBot_V0.5.py (AnaylsisAiBotStreamlit.py is not 0.5v, but experiment version):

Fix the critical bugs that bring the wrong order files from path. ->  previous (lesser than 20 percent accurancy) - > near to 60 percent.

AnalysisAiBot_V0.6.py 

until 0.5V ,  img -> text(explanation) -> tag
0.6v   img-> tag (direct)


AnalysisAib0t_V0.7.py = MultipleImgsAi_v0.7.py


AnalysisAib0t_V0.8.py -> defalut temperature 0.3->0.25, make integra function to make it readable.



## 3. Main.py (FastAPi)

V0.1 -> just conver to Fast api (no main page)
V0.2 -> main page (mini test)
V0.3 -> temperature default changed, use integrated function


## 4. others
  demoaivision.py -> basic api how to use img file

  imagepath.py  -> path printer (see order of the files)

  imgAi.py -> single img with simple prompt
