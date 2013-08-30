function word_cloud(selector) {
    var colours = {
        'blue': ['#80CCFF', '#0099ff', '#0F93D3', '#0066cc', 
                '#0D68AF', '#333399', '#0E3282'],
        'orange': ['#FFE05C', '#ffcc00', '#F2AC3A', '#ff9933', 
                '#EA8746', '#ff3333', '#913F31'],
        'green': ['#7DAA43', '#99cc33', '#7CBC4E', '#009933', 
                '#2AAB51', '#009966', '#1E593B'],
        'red': ['#FF9494', '#cc3333', '#C21833', '#990000', 
                '#8C181B', '#660000', '#380100']
    };

    var colours_indices = [];
    for (var i = 0; i <= colours['blue'].length; i++) {
        colours_indices.push(i);
    }

    var target = d3.select(selector);
    var palette = colours[target.attr('data-colour') || 'green'];
    var fill = d3.scale.ordinal().domain(colours_indices).range(palette);
    var text_scale = parseFloat(target.attr('data-text-scale')) || 1;
    var spiral = target.attr('data-spiral') || 'archimedean';
    var font = target.attr('data-font') || 'Georgia,serif';
    var no_rotate_chance = parseFloat(target.attr('data-no-rotate-chance')) || 0.65;

    var domElement = target[0][0];
    var width = domElement.offsetWidth;
    var height = domElement.offsetHeight;
    
    var words = jQuery.parseJSON(target.attr('data-keywords'));
    var max = words[0].size;
    var fill_fns = {
        size: function(d, i) { return fill(d.size/max * 6); },
        index: function(d, i) { return fill(words[i].colour); },
        custom: function(d, i) { return words[i].colour; }
    };
    var fill_fn = fill_fns[target.attr('data-fill') || 'size'];

    //var application_url = d3.select('link[rel="application-url"]').attr('href');

    function draw(words) {
        target.append("svg")
              .attr("width", width)
          .attr("height", height)
            .append("g")
              .attr("transform", "translate("+ width/2 + "," + height/2 + ")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
              .style("font-size", function(d) { return d.size + "px"; })
              .style("fill", fill_fn)
          .attr("id", function(d, i) { return "word-cloud-tag-" + i; })
              .attr("text-anchor", "middle")
              .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
              })
            .text(function(d) { return d.text; })
        .on('click', function(d) { 
     //   window.location = application_url + 'test'; 
        });
    }
    d3.layout.cloud()
      .size([width, height])
      //.startPoint([width/2, height/2])
          .words(words)
      .timeInterval(10)
      .spiral(spiral)
          .rotate(function(d, i) {
              return i === 0 ? 0 : Math.ceil(Math.random() - no_rotate_chance) * 90; 
          })
          .font(font)
          .fontSize(function(d) { 
              var size = d.size/max * text_scale; 
              return size > 10 ? size : 10;
          })
          .on("end", draw)
          .start();
}

jQuery(function($){
    //Only load D3-based word cloud if SVG support 
    var selector = '.word-cloud';
    if (typeof Modernizr === 'undefined' || (Modernizr && Modernizr.svg)) {
        word_cloud(selector);
    } else {
        $(selector).text('Your browser does not support SVG. :(');
    }
});
