var width = 500, height = 500;

$(function() {
  var fill = d3.scale.category20();

  var submit_form = function(e) {
    $.getJSON($SCRIPT_ROOT + '/_cloudify', {
      minsyl: $('select[id="minsyl"] option:selected').val(),
      ntags: $('select[id="ntags"] option:selected').val(),
      rotated: $('select[id="rotated"] option:selected').val(),
      tagger : $('select[id="tagger"] option:selected').val(),
      text: $('textarea[id="wordtext"]').val(),
      posnv: ($('input[id="noun"]:checked').val() || '') +
             ($('input[id="verb"]:checked').val() || '')
    }, function(data) {
      d3.layout.cloud().size([width, height])
        .words(data.tags)
        .padding(5)
        .rotate(function() { return ~~(Math.random() * 2) * 90 * data.rotated; })
        .fontSize(function(d) { return d.size; })
        .on("end", draw)
        .start();

      $("#info").empty();
      var info = d3.select("#info");
      info.append("span").text("Time: " + Math.round(data.time*100)/100 + "s");
      info.append("span").text("Text length: " + data.textlen);
      info.append("span").text("POS: " + data.posnv);
      info.append("span").text("ntags: " + data.ntags);

      var bgcolor = $('select[id="bgcolor"] option:selected').val();
      var font = $('select[id="custom-font"] option:selected').val();
      var style = document.createElement('style');
      style.type = 'text/css';
      style.innerHTML = "div#wordcloud { background-color: " + bgcolor + "; } div#wordcloud text { font-family: " + font + "; }";
      document.getElementById('wordcloud').appendChild(style);

    });

    return false;
  };

  $('form#button-create').bind('click', submit_form);

  function draw(words) {
    $("div#wordcloud").empty(); // clear div before generating
    d3.select("div#wordcloud").append("svg")
        .attr("width", width)
        .attr("height", height)
      .append("g")
        .attr("transform", "translate(250,250)")
      .selectAll("text")
        .data(words)
      .enter().append("text")
        .style("font-size", function(d) { return d.size + "px"; })
        .style("fill", function(d, i) { return fill(i); })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
      .text(function(d) { return d.text; });
  }
});
