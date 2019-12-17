/* eslint-env browser */
<template>
    <div style="margin : 15px;">
        <h3 style="margin-left:450px;font-weight: bold;font-size: 90px;margin-bottom: 10px;margin-top:30px; ">
            
        </h3>
        <div id="chart">
        </div>
    </div>
</template>

<script>

import * as d3 from "d3";
import "d3-selection-multi";
//import brandData from "../assets/linedummy.json";
import stockdata from "../assets/stockdata.json"

export default {
    name : "LineChart",
    data(){
        return{
            stockdata
        }
    },
    methods : {
        renderChart : function(){
            
            var parseDate = d3.timeParse("%b %Y");
            stockdata.forEach(d => {
                d.price = isNaN(d.price) ? 0 : d.price,
                d.date = parseDate(d.date)
            });

            // Filter to one symbol; the S&P 500.
            var values = stockdata.filter(function(d) {
                return d.symbol == "AMZN";
            });

            const getImgUrl = function(imagename) {
                let result;
                try {
                    result = require("../assets/images/"+imagename+".png");
                }
                catch (e) {
                    result  = undefined;
                }
                return result;
            }

            /*var extendXaxis = function(data,xaxis_name,limit){
                let data_length = data.length;
                let last_xaxis_value = data[data_length][xaxis_name];
                let previous_xaxis_value = data[data_length][xaxis_name];
        
                if(typeof(last_xaxis_value) == "Number"){
                let previous_xaxis_value = data[data_length][xaxis_name];
                    var diff = last_xaxis_value-previous_xaxis_value;

                }
                else if(typeof(last_xaxis_value) == "String"){
                    var date_last = parseDate(last_xaxis_value);
                    var date_prev = parseDate(previous_xaxis_value);
                    const diffTime = Math.abs(date_last - date_prev);
                    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

                }

            }*/
            //console.log(values);

            var limit = 60;
            var counter = 0;
            var data_reduction_factor = 3/5;
            let data = values.slice(0,limit)

            //console.log(data);

            //var duration = 2000;
            //now = new Date(Date.now() - duration);
            //data = window.data = d3.range(n).map(function() { return 0; });

            var margin = {top: 6, right: 40, bottom: 20, left: 40},
                width = window.innerWidth - margin.right,
                height = (window.innerHeight/2) ;
            
            var x = d3.scaleTime()
                .domain(d3.extent(data, function(d) { return d.date; }))
                .range([0, width]);

            var y = window.y = d3.scaleLinear()
                .range([height, 0]);

            var line = d3.line()
                .curve(d3.curveBasis)
                .x(function(d, i) { return x(d.date); })
                .y(function(d, i) { return y(d.price); });

            var svg = d3.select("body").append("p").append("svg")
                .attr("width", width + margin.left + margin.right - 100)
                .attr("height", height + margin.top + margin.bottom+40)
            .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            svg.append("defs").append("clipPath")
                .attr("id", "clip")
            .append("rect")
                .attr("width", width)
                .attr("height", height);

            var xaxis = svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(x.axis = d3.axisBottom().scale(x));

            var yaxis = svg.append("g")
                .attr("class", "y axis")
                .attr("transform", "translate(" + margin.left + ", 0)")
                .call(y.axis = d3.axisLeft().scale(y).ticks(5));

            var path = svg.append("g")
                .attr("class", "path container")
                .attr("clip-path", "url(#clip)")
            .append("path")
                .data([data])
                .attr("class", "line");

            var image = svg.append("svg:image")
                .data([data])
                .attr('dx', -40)
                .attr('dy', -100)
                .attr('width', 100)
                .attr('height', 100)
                .attr("transform", "translate(" + (width - margin.left - margin.right) +", " + y(0) + ")")
                .attr("xlink:href", getImgUrl("amzn"))
            
            var name = svg.append("text")
                .data([data])
                .attr('dx', 8)
                .attr('dy', 3)
                .attr("transform", "translate(" + (width - margin.left - margin.right) +", " + y(0) + ")")
                .style('text-anchor', 'start')
                .text("Amzn")

            //var previous_to_previous_start = data[0].date;
            var previous_date_start = data[0].date;
            //counter = 1;
            var lineData = [];
            lineData.push(data[0]);
            var duration_speed = 100;

            tick();

            function tick() {   

                //console.log("new");
                //console.log(lineData);
                counter = counter+1;
                previous_date_start = data[0].date;
                var fillInitial = true;
                //var lineData = [];//data.slice(0,3*limit/4);
            
                if(values.length > counter){
                    //console.log("sebin "+counter)
                    if(fillInitial && lineData.length < (data.length)*data_reduction_factor){
                        console.log("sebin this is too much"+counter)
                        lineData.push(data[counter]);
                        duration_speed = 300;
                    }
                    else{
                        //console.log(data[data.length-1]);
                        console.log("sebin "+counter)
                        //console.log(values[counter-1]);
                        fillInitial = false;
                        data = data.slice(1-data.length).concat(values[(limit-(limit*data_reduction_factor))+counter-1]);
                        //lineData =[];
                        /*if((values.length - data.length) < ){

                        }*/
                        lineData = data.slice(0,data_reduction_factor*limit);
                        duration_speed = 800;
                        //console.log(values[counter-1]);
                        //console.log(data);
                    }
                }
                
                
                // update the domains
                //now = new Date();
                x.domain(d3.extent(data, function(d) { return d.date; }));
                y.domain([d3.min(values, function(d) { return d.price; }), d3.max(values, function(d) { return d.price; })]);

                // push the accumulated count onto the back, and reset the count

                console.log(lineData); //data.slice(1-data.length).concat(values[counter-1]);
                
                // redraw the line
                svg.select(".line")
                    .attr("d", line(lineData))
                    .transition()
                    .ease(d3.easeLinear)
                    .attr("transform", null)
                    .style("stroke","red")
                    .style("fill", "none");

                // slide the x-axis left
                xaxis.transition()
                    .duration(duration_speed)
                    .ease(d3.easeLinear)
                    .call(x.axis);

                yaxis.call(y.axis);

                name.transition()
                    .duration(10)
                    .attr("transform", function(d) { 
                        return "translate(" + x(lineData[lineData.length-2].date)+5 +", " + y(lineData[lineData.length-1].price+10) + ")"})
                    .text("Amzn");

                image.transition()
                    .duration(10)
                    .attr("transform", function(d) { 
                        return "translate(" + x(lineData[lineData.length-2].date)+5 +", " + y(lineData[lineData.length-1].price+10) + ")"});

                // slide the line left
                path.transition()
                    .duration(duration_speed)
                    .ease(d3.easeLinear)
                    .attr("transform", "translate(" + x(previous_date_start) + ")")
                    .on("end", tick);


                // pop the old data point off the front

        }
            //http://bl.ocks.org/atmccann/8966400

        }
    },
    mounted (){
        this.renderChart();
    }
}

</script>

<style>
    text{
        font-size: 50px;
        font-family: Open Sans, sans-serif;
    }
</style>
