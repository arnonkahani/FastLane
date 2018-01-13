
// create a map
var map = L.map('map').setView([31.7702, 35.2263], 13);
map.setMaxBounds(map.getBounds());
mapLink = 
    '<a href="http://openstreetmap.org">OpenStreetMap</a>';
L.tileLayer(
    'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; ' + mapLink + ' Contributors',
    maxZoom: 18,
    }).addTo(map);
            
/* Initialize the SVG layer */
map._initPathRoot()    

var svg = d3.select("#map").select("svg"),
    g = svg.append("g");

map.on('click', addMarker);

var markers = [];
var markersLayer = new L.LayerGroup();
var linesLayer = new L.LayerGroup();

function addMarker(e){
    var newMarker = new L.circleMarker(e.latlng, {radius: 6}).addTo(markersLayer);
        markersLayer.addTo(map);
        markers.push([e.latlng.lat, e.latlng.lng]);
        if (markers.length > 1){
            var polyline = new L.Polyline(markers, {
                color: 'red',
                weight: 2.5,
                opacity: 0.5,
                smoothFactor: 1
                });
            polyline.addTo(linesLayer);
            linesLayer.addTo(map);
        }
}

function sendData(){
    if(markers.length === 0){
        alert("Please mark a route on the map");
    }
    else{
        axios.defaults.headers.common['Access-Control-Allow-Origin'] = "*"
        axios({
            method: 'post',
            url: '/compute',
            data: markers
          })
        .then(function (response) {
            console.log(response.data);
            showResults(response.data);
        })
        .catch(function (error) {
          console.log(error);
        });
    }
}

function clearData(){
    markersLayer.clearLayers();
    linesLayer.clearLayers();
    markers = [];
}

function showResults(res){

  // create the bar chart general properties
  var margin = {top: 20, right: 20, bottom: 70, left: 40},
      width = 500 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

  var	parseDate = d3.time.format("%H:%M").parse;

  var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);
  var y = d3.scale.linear().range([height, 0]);

  var xAxis = d3.svg.axis()
  .scale(x)
  .orient("bottom")
  .tickFormat(d3.time.format("%H:%M"));

  var yAxis = d3.svg.axis()
  .scale(y)
  .orient("left")
  .ticks(10);

  // create bar chart for each stop
//   d3.json("test.json", function(error, data) {
    res.forEach(function(stop) {

      // create stops markers
      L.marker( [stop.lat, stop.lng], {title: stop.stopName} ).addTo(markersLayer);

      // create a svg for each stop
      var svg = d3.select("body")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", 
              "translate(" + margin.left + "," + margin.top + ")");

      stop.numberOfTrips.forEach(function(d) {
          d.hour = parseDate(d.hour);
          d.numOfTripsPerHour = +d.numOfTripsPerHour;
      });

      // define the domain for each axis
      x.domain(stop.numberOfTrips.map(function(d) { return d.hour; }));
      y.domain([0, d3.max(stop.numberOfTrips, function(d) { return d.numOfTripsPerHour; })]);

      // add title for each bar chart
      svg.append("text")
      .attr("x", (width / 2))             
      .attr("y", 0 - (margin.top/3))
      .attr("text-anchor", "middle")  
      .style("font-size", "16px") 
      .style("text-decoration", "underline")  
      .text("Stop Name: "+ stop.stopName);

      // define x axis
      xTitle = svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", "-.55em")
        .attr("transform", "rotate(-90)");

      svg.append("text")
        .attr("class", "x label")
        .attr("text-anchor", "middle")
        .attr("x", width/2)
        .attr("y", height+(margin.bottom/1.5))
        .text("hours");

      // define y axis
      svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

      svg.append("text")
        .attr("class", "y label")
        .attr("text-anchor", "middle")
        .attr("x", 0-(margin.left/1.3))
        .attr("y", height/2)
        .text("V");

      // create a tip
      var tip = d3.tip()
      .attr('class', 'd3-tip')
      .offset([-10, 0])
      .html(function(d) {
        return "<strong>V:</strong> <span style='color:rgb(233, 204, 38)'>" + d.numOfTripsPerHour + "</span>";
      });

      svg.call(tip);

      // create bars
      svg.selectAll("bar")
        .data(stop.numberOfTrips)
        .enter()
      .append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.hour); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.numOfTripsPerHour); })
        .attr("height", function(d) { return height - y(d.numOfTripsPerHour); })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);
    });
  //});

  // add the stops markers to the map
  markersLayer.addTo(map);
}

