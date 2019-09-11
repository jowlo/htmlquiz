#!/bin/python3

import json
import argparse

COLORS = [
    ("rgba(91, 192, 235, 1)", "rgba(195, 232, 247, 1);"),
    ("rgba(253, 231, 76, 1);", "rgba(254, 246, 189, 1);"),
    ("rgba(155, 197, 61, 1);", "rgba(218, 233, 184, 1);"),
    ("rgba(195, 66, 63, 1);", "rgba(233, 186, 185, 1);")
]


def color_styles():
    return "\n".join(["""
.question.cat{cat} {{
  background: {color};
}}

.answer.cat{cat} {{
  background: #424242;
  color: {color};
}}

a:visited.overview-link.cat{cat} {{
  background: #878787;
  color: {color_visited};
}}

a:visited .question.cat{cat} {{
  background: {color_visited};
  color: #878787;
}}""".format(cat=i, color=color[0], color_visited=color[1])
                      for i, color in enumerate(COLORS)])


def overview_headings(data):
    return "\n".join(["<td class=overview-head>{name}</td>".format(name=cat)
                      for cat in sorted(data['categories'].keys())])


def overview_cells(data):
    ret = ""

    max_questions = max([len(qs) for qs in data['categories'].values()])

    for qvalue in range(max_questions):
        ret += """
        <tr>"""
        for qcat in range(len(data['categories'])):
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
          </td>""".format(qcat=qcat, qvalue=qvalue+1,
                          qvalueprint=(qvalue + 1) * 100)
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
        for qcat in range(len(data['categories'])):
            cat = sorted(data['categories'].keys())[qcat]
            if(len(data['categories'][cat]) > qvalue):
                ret += """
  <a href="#a{qcat}-{qvalue}">
    <div id="q{qcat}-{qvalue}" class="screen">
      <div class="centered bigone question cat{qcat}">
          {question}
      </div>
    </div>
  </a>""".format(question=data['categories'][cat][qvalue]['question'],
                 qvalue=qvalue+1, qcat=qcat)
    return ret


def answers(data):
    max_questions = max([len(qs) for qs in data['categories'].values()])
    ret = ""
    for qvalue in range(max_questions):
        for qcat in range(len(data['categories'])):
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
  </a>""".format(answer=data['categories'][cat][qvalue]['answer'],
                 qvalue=qvalue+1, qcat=qcat)
    return ret


def main():
    parser = argparse.ArgumentParser(
        description='Generate a clickable HTML/JS quiz for use on a beamer.')
    parser.add_argument('config', help="JSON configuration file")
    args = parser.parse_args()

    with open(args.config, "r") as config, open("base.html", "r") as basefile:
        data = json.load(config)
        base = basefile.read()

        print(base.format(
            color_styles=color_styles(),
            overview_headings=overview_headings(data),
            overview_cells=overview_cells(data),
            questions=questions(data),
            answers=answers(data)
        ))


if __name__ == "__main__":
    main()
