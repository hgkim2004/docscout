var width = 500, height = 500;

$(function() {
  var fill = d3.scale.category20();

  var submit_form = function(e) {
    $.getJSON($SCRIPT_ROOT + '/_cloudify', {
      text: $('textarea[id="wordtext"]').val()
    }, function(data) {
      d3.layout.cloud().size([width, height])
        .words(data.tags)
        .padding(5)
        .rotate(function() { return ~~(Math.random() * 2) * 90; })
        .font("Impact")
        .fontSize(function(d) { return d.size; })
        .on("end", draw)
        .start();
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
        .style("font-family", "Impact")
        .style("fill", function(d, i) { return fill(i); })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; });
  }
});
