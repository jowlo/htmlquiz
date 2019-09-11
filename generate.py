#!/bin/python3

import json

colors = [
"rgba(91, 192, 235, 1)",
"rgba(253, 231, 76, 1);",
"rgba(155, 197, 61, 1);",
"rgba(195, 66, 63, 1);"
]
colors_visited = [
"rgba(195, 232, 247, 1);",
"rgba(254, 246, 189, 1);",
"rgba(218, 233, 184, 1);",
"rgba(233, 186, 185, 1);"
]


def color_styles():
    ret = "\n".join(["""
.question.cat{cat} {{
  background: {col};
}}

.answer.cat{cat} {{
  background: #424242;
  color: {col};
}}""".format(cat=i, col=color) for i, color in enumerate(colors)])

    ret += "\n".join(["""
a:visited.overview-link.cat{cat} {{
  background: #878787;
  color: {col};
}}

a:visited .question.cat{cat} {{
  background: {col};
  color: #878787;
}} """.format(cat=i, col=color) for i, color in enumerate(colors_visited)])
    return ret


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
            <a class="overview-link question cat{qcat}" href="#q{qcat}-{qvalue}">
              <div class="overview-centered">
                {qvalueprint}
              </div>
              <span class="status right" id="q{qcat}-{qvalue}-right">✔</span><span class="status wrong" id="q{qcat}-{qvalue}-wrong">⨯</span>
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
      <div class="centered bigone question cat{qcat}">
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
      <div class="bigone answer cat{qcat}">
        <div class="centered">{answer}</div>
        <div>
          <div class="status right" onclick="document.getElementById('q{qcat}-{qvalue}-right').style.display = 'block';">✔</div>
          <div class="status wrong" onclick="document.getElementById('q{qcat}-{qvalue}-wrong').style.display = 'block';">⨯</div>
        </div>
      </div>
    </div>
  </a>""".format(answer=data['categories'][cat][qvalue]['answer'], qvalue=qvalue+1,
                 qcat=qcat)
    return ret

print(base.format(
    color_styles=color_styles(),
    overview_headings=overview_headings(data),
    overview_cells=overview_cells(data),
    questions=questions(data),
    answers=answers(data)
))
