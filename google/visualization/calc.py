# -*- coding: utf-8 -*-
# Copyright 2010 Yu Watanabe. All Rights Reserved.

import copy
import StringIO
import sys

kStartYear = 2009
kEndYear = 2080


class Stat(object):
  def __init__(self, population=0.0, deathrate=0.0, birthrate=0.0):
    self.population = population
    self.deathrate = deathrate
    self.birthrate = birthrate

  def __str__(self):
    return '(p=%f,d=%f,b=%f)' % (self.population,
                                 self.deathrate,
                                 self.birthrate)


def read_file(filename):
  results = []
  f = file(filename)
  for l in f.readlines():
    l = l.strip()
    if len(l) == 0 or l.startswith('#'):
      continue
    values = map(float, l.split(','))
    values[0] = int(values[0])
    results.append(tuple(values))
  assert len(results) > 0
  return results


def read_data():
  population = read_file('data/population')
  deathrate = read_file('data/death_rate')
  birthrate = read_file('data/birth_rate')
  max_age = 0
  max_age = max(max_age, population[len(population) - 1][0])
  max_age = max(max_age, deathrate[len(deathrate) - 1][0])
  max_age = max(max_age, birthrate[len(birthrate) - 1][0])
  men = []
  women = []
  for i in xrange(max_age + 1):
    men.append(Stat())
    women.append(Stat())
  for e in population:
    men[e[0]].population = e[1]
    women[e[0]].population = e[2]
  for e in deathrate:
    men[e[0]].deathrate = e[1]
    women[e[0]].deathrate = e[2]
  for e in birthrate:
    men[e[0]].birthrate = 0.0
    women[e[0]].birthrate = e[1]
  return men, women


def next_step(men, women):
  for i in xrange(len(men) - 1):
    n = len(men) - i - 1
    men[n].population = men[n-1].population * (1.0 - men[n - 1].deathrate)
  baby = 0.0
  for i in xrange(len(women) - 1):
    n = len(women) - i - 1
    baby += women[n].population * women[n].birthrate
    women[n].population = women[n-1].population * (1.0 - women[n - 1].deathrate)

  male_ratio = men[0].population / (men[0].population + women[0].population)
  men[0].population = baby * male_ratio
  women[0].population = baby * (1 - male_ratio)



kPyramidTemplate = '''
<html>
  <head>
    <title>日本の人口ピラミッドの予測</title>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load('visualization', '1', {'packages':['motionchart']});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Age');
        data.addColumn('number', 'Year');
        data.addColumn('number', 'Age');
        data.addColumn('number', 'Population');
        data.addColumn('string', 'Sex');
        data.addRows([
          %s
          ]);
        var chart = new google.visualization.MotionChart(document.getElementById('chart_div'));
        chart.draw(data, {width: 900, height:600});
      }
    </script>
  </head>

  <body>
    <div style="width:600px">
      2009年の年齢別の人口・出生率・死亡率にもとづく，日本の人口ピラミッドの変化の予測．
      Google Visualization API を使ってアニメーション化．
      ソースコードは
      <a href="https://github.com/yunabe/practice/tree/master/google/visualization/data">こちら</a>．

      <ul>
       <li><a href="population.html">日本の人口数の予測</a></li>
       <li><a href="ratio.html">日本の人口比率の予測</a></li>
      </ul>
    </div>
    <div id="chart_div" style="width: 900px; height: 600px;"></div>
  </body>
</html>
'''

def export_pyramid(men, women):
  rows = StringIO.StringIO()
  for year in xrange(kStartYear, kEndYear):
    rows.write(export_pyramid_row(year, men, women))
    next_step(men, women)
  return kPyramidTemplate % rows.getvalue().rstrip(',')


def export_pyramid_row(year, men, women):
  o = StringIO.StringIO()
  for i, s in enumerate(men):
    o.write('["Male: %d", %d, %d, %f, "Male"],' % (year - i, year, i,
                                                   s.population))
  for i, s in enumerate(women):
    o.write('["Female: %d", %d, %d, %f, "Female"],' % (year - i, year, i,
                                                       s.population))
  return o.getvalue()


kAreaChartTemplate = '''
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Year');
        %s
        data.addRows([
          %s
        ]);

        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
        chart.draw(data, {width: 900, height: 600, title: 'Company Performance',
                          vAxis: {minValue: 0},
                          hAxis: {title: 'Year', titleTextStyle: {color: '#FF0000'}}
                         });
      }
    </script>
  </head>
  <body>
    <div id="chart_div"></div>
  </body>
</html>
'''

kImportantAges = [0, 15, 65]

def get_area_chart_column_defs(max_age):
  o = StringIO.StringIO()
  age = 0
  for age in kImportantAges:
    if age > max_age:
      break
    o.write('data.addColumn("number", "%d <=");' % age)
  return o.getvalue()


def export_population_or_ratio_row(year, max_age, men, women, is_ratio):
  o = StringIO.StringIO()
  total = sum(map(lambda x: x.population, men + women))
  if is_ratio:
    normalizer = 1 / total
  else:
    normalizer = 1.0
  age = 0
  o.write('["%d"' % year)
  for i in xrange(len(kImportantAges)):
    age = kImportantAges[i]
    if age > max_age:
      break
    o.write(', %f' % (total * normalizer))
    if i < len(kImportantAges) - 1:
      next_age = kImportantAges[i + 1]
      total -= sum(map(lambda x: x.population, men[age:next_age]))
      total -= sum(map(lambda x: x.population, women[age:next_age]))
  o.write('],')
  return o.getvalue()


def export_population_or_ratio(men, women, is_ratio):
  max_age = max(len(men) - 1, len(women) - 1)
  column_defs = get_area_chart_column_defs(max_age)
  rows = StringIO.StringIO()
  for year in xrange(kStartYear, kEndYear):
    rows.write(export_population_or_ratio_row(
        year, max_age, men, women, is_ratio))
    next_step(men, women)
  return kAreaChartTemplate % (column_defs, rows.getvalue().rstrip(','))


kLineChartTemplate = '''
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Year');
        %s
        data.addRows(%d);
        %s
        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, {width: 900, height: 600, title: 'Eligibility Age',
                          vAxis: {minValue: 55},
                          hAxis: {title: 'Year', titleTextStyle: {color: '#FF0000'}}
                         });
      }
    </script>
  </head>
  <body>
    <div id="chart_div"></div>
  </body>
</html>
'''

def calc_eligibility_age(men, women, start_age, num):
  population = sum(map(lambda m:m.population, men + women))
  young_population = sum(
    map(lambda m:m.population, men[:start_age] + women[:start_age]))
  young_rate = 1.0 * young_population / population

  setvalues = []
  for year in xrange(kStartYear, kEndYear):
    population = sum(map(lambda m:m.population, men + women))
    young_population = 0
    for i in xrange(len(men)):
      pop_i = men[i].population + women[i].population
      if population * young_rate > young_population + pop_i:
        young_population += pop_i
      else:
        age = i + (population * young_rate - young_population) / pop_i
        break
    setvalues.append(
      'data.setValue(%d, %d, %f);' % (year - kStartYear, num, age))
    next_step(men, women)
  return young_rate, setvalues


def export_eligibility_age(men, women):
  ages = [65, 60, 55,]
  allsetvalues = []
  for year in xrange(kStartYear, kEndYear):
    allsetvalues.append('data.setValue(%d, 0, "%d");' % (year - kStartYear,
                                                         year))
  addcolumns = []
  for i, age in enumerate(ages):
    young_rate, setvalues = calc_eligibility_age(
      copy.deepcopy(men), copy.deepcopy(women), age, i + 1)
    allsetvalues.extend(setvalues)
    label = 'Top %.2f - (%d years old in %d)' % (100 - 100.0 * young_rate,
                                               age, kStartYear)
    addcolumns.append('data.addColumn("number", "%s");' % label)

  return kLineChartTemplate % ('\n'.join(addcolumns),
                               len(allsetvalues) / (len(ages) + 1),
                               '\n'.join(allsetvalues))


def main():
  assert len(sys.argv) == 2
  mode = sys.argv[1]
  men, women = read_data()
  if mode == 'pyramid':
    print export_pyramid(men, women)
  elif mode == 'population':
    print export_population_or_ratio(men, women, False)
  elif mode == 'ratio':
    print export_population_or_ratio(men, women, True)
  elif mode == 'eligibility':
    print export_eligibility_age(men, women)
  else:
    print >> sys.stderr, 'Invalid mode:', mode
    sys.exit(1)


if __name__ == '__main__':
  main()
