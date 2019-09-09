#!/bin/python3

import json

with open("config.json", "r") as config:
    data = json.load(config)

with open("base.html", "r") as basefile:
    base = basefile.read()

num_cat = len(data['categories'])


def overview_headings(data):
    return "\n".join(["<td class=overview-head>{name}</td>".format(name=cat)
                      for cat in sorted(data['categories'].keys())])

def overview_cells(data):
    ret = ""

    max_questions = max([len(qs) for qs in data['categories'].values()])

    for qvalue in range(max_questions):
        ret += """
        <tr>"""
        for qcat in range(num_cat):
            cat = sorted(data['categories'].keys())[qcat]
            if(len(data['categories'][cat]) > qvalue):
                ret += """
          <td class="overview-cell">
            <a class="overview-link question" href="#q{qcat}-{qvalue}">
              <div class="centered">
                {qvalueprint}
              </div>
            </a>
          </td>""".format(qcat=qcat, qvalue=qvalue+1, qvalueprint=(qvalue+1)*100)
            else:
                ret += """
          <td class="overview-cell">
          </td>"""

        ret += """
        </tr>"""

    return ret


def questions(data):
    max_questions = max([len(qs) for qs in data['categories'].values()])
    ret = ""
    for qvalue in range(max_questions):
        for qcat in range(num_cat):
            cat = sorted(data['categories'].keys())[qcat]
            if(len(data['categories'][cat]) > qvalue):
                ret += """
  <a href="#a{qcat}-{qvalue}">
    <div id="q{qcat}-{qvalue}" class="screen">
      <div class="centered bigone question">
          {question}
      </div>
    </div>
  </a>""".format(question=data['categories'][cat][qvalue]['question'], qvalue=qvalue+1,
                 qcat=qcat)
    return ret


def answers(data):
    max_questions = max([len(qs) for qs in data['categories'].values()])
    ret = ""
    for qvalue in range(max_questions):
        for qcat in range(num_cat):
            cat = sorted(data['categories'].keys())[qcat]
            if(len(data['categories'][cat]) > qvalue):
                ret += """
  <a href="#overview">
    <div id="a{qcat}-{qvalue}" class="screen">
      <div class="centered bigone answer">
        {answer}
      </div>
    </div>
  </a>""".format(answer=data['categories'][cat][qvalue]['answer'], qvalue=qvalue+1,
                 qcat=qcat)
    return ret

print(base.format(
    overview_headings=overview_headings(data),
    overview_cells=overview_cells(data),
    questions=questions(data),
    answers=answers(data)
))
