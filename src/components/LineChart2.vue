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
import stockdata from "../assets/stockdata.json"
import event_lists from "../assets/event_list.json"

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

            /*var extendXaxis = function(data,xaxis_name,limit,factor){
                let prefix_len = limit*(1-factor);
                let post_len = limit*factor;
                let data_length = data.length;
                let last_xaxis_value = data[data_length-1][xaxis_name];
                //let previous_xaxis_value = data[data_length-2][xaxis_name];
        
                if(typeof(last_xaxis_value) == "Number"){
                let previous_xaxis_value = Number(data[data_length][xaxis_name]);
                    var diff = Number(last_xaxis_value)-previous_xaxis_value;
                    
                }
                else if(typeof(last_xaxis_value) == "String"){
                    var date_last = parseDate(last_xaxis_value);
                    var date_prev = parseDate(previous_xaxis_value);
                    const diffTime = Math.abs(date_last - date_prev);
                    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

                }

            }*/

            var limit = 60;
            var counter = 0;
            var data_reduction_factor = 3/5;
            let data = values.slice(0,limit)

            var margin = {top: 300, right: 40, bottom: 20, left: 80},
                width = 3600 - margin.right,
                height = (window.innerHeight/2+300) ;
            
            var x = d3.scaleTime()
                .domain(d3.extent(data, function(d) { return d.date; }))
                .range([0, width]);

            var y = window.y = d3.scaleLinear()
                .range([height, 0]);

            var line = d3.line()
                .curve(d3.curveBasis)
                .x(function(d, i) { 
                    return x(d.date); })
                .y(function(d, i) { 
                    return y(d.price); 
                });

            var svg = d3.select("body").append("p").append("svg")
                .attr("width", width + margin.left + margin.right - 10)
                .attr("height", height + margin.top + margin.bottom+40)
            .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            svg.append("defs").append("clipPath")
                .attr("id", "clip")
            .append("rect")
                .attr("width", width)
                .attr("height", height);

            var xaxis = svg.append("g")
                .attr("class", "xAxis")
                .attr("transform", "translate(0," + height + ")")
                .call(x.axis = d3.axisBottom().scale(x));

            var yaxis = svg.append("g")
                .attr("class", "yAxis")
                .attr("transform", "translate(" + margin.left + ", 0)")
                .call(y.axis = d3.axisLeft().scale(y).ticks(5));

            // Clipping start here
            var path = svg.append("g")
                .attr("class", "path container")
                .attr("clip-path", "url(#clip)")
            .append("path")
                .data([data])
                .attr("class", "line");


            // Appending various elements to svg
            var yearText = svg.append("text")
                .data([data])
                .attrs({
                    class: 'yearText',
                    x: width-750,
                    y: height-100
                })
                .style('text-anchor', 'start')

            var image = svg.append("svg:image")
                .data([data])
                .attr('dx', -40)
                .attr('dy', -100)
                .attr('width', 80)
                .attr('height', 80)
                .attr("transform", "translate(" + (width - margin.left - margin.right) +", " + y(0) + ")")
                .attr("xlink:href", getImgUrl("amzn"))
            
            var name = svg.append("text")
                .data([data])
                .attr('class','ticker')
                .attr('dx', 8)
                .attr('dy', 3)
                .attr("transform", "translate(" + (width - margin.left - margin.right) +", " + y(0) + ")")
                .style('text-anchor', 'start')

            // -------------------------------------------
            // Logic for event addition
            // -------------------------------------------
            var tipList = [];
            for(var tips in event_lists){
                tips;
                var tip = svg.append("svg:image")
                    .data([event_lists])
                    .attr('dx', -40)
                    .attr('dy', -100)
                    .attr('width', 80)
                    .attr('height', 80)
                    .attr("transform", "translate(" + -200 +", " + y(500) + ")")
                    .attr("xlink:href", getImgUrl("amzn"));
                tipList.push(tip);
            }

            // -------------------------------------------
            // Logic for dashboard
            // -------------------------------------------



            // ----------------------------------------
            // declarations for tick function
            // ----------------------------------------            
            var lineData = [];
            lineData.push(data[0]);
            var duration_speed = 100;

            tick();

            function tick() {   

                counter = counter+1;
                var previous_date_start = data[0].date;

                // ----------------------------------------
                // resetting domain
                // ---------------------------------------- 
                if(values.length > counter){
                    data = data.slice(1-data.length).concat(values[limit+counter-1]);
                    lineData = data.slice(0,data_reduction_factor*limit);
                    duration_speed = 800;
                }
                
                x.domain(d3.extent(data, function(d) { return d.date; }));
                y.domain([d3.min(values, function(d) { return d.price; }), d3.max(values, function(d) { return d.price; })]);

                // ----------------------------------------
                // redrawing line
                // ---------------------------------------- 
                svg.select(".line")
                    .attr("d", line(lineData))
                    .transition()
                    .ease(d3.easeLinear)
                    .attr("transform", null);

                // slide the x-axis left
                xaxis.transition()
                    .duration(duration_speed)
                    .ease(d3.easeLinear)
                    .call(x.axis);

                yaxis.call(y.axis);
                
                // ----------------------------------------
                // elements animation
                // ---------------------------------------- 
                yearText.text(d =>{
                    return d3.timeFormat("%Y %b")(lineData[lineData.length-1].date)
                    });

                name.text(d =>{
                    return lineData[lineData.length-1].price
                    })
                    .transition()
                    .duration(100)
                    .attr("transform", function(d) { 
                        return "translate(" + x(lineData[lineData.length-2].date) +", " + y(lineData[lineData.length-1].price-4) + ")"});

                image.transition()
                    .duration(10)
                    .attr("transform", function(d) { 
                        return "translate(" + x(lineData[lineData.length-2].date)+5 +", " + y(lineData[lineData.length-1].price+7) + ")"}); 

                for(var i=0;i<tipList.length;i++){
                    
                    console.log(tipList[0]);
                    tipList[i].transition()
                        .duration(duration_speed)
                        .ease(d3.easeLinear)
                        .attr("transform", function(d) { 
                            let xValue = x(parseDate(d[i].date));
                            let yValue = parseDate(d[i].date) < lineData[lineData.length-1].date ? y(d[i].price+20) : -500;
                            return "translate(" + xValue +", " + yValue + ")"
                        });
                }
                

                // ----------------------------------------
                // Path transition
                // ---------------------------------------- 
                path.transition()
                    .duration(duration_speed)
                    .ease(d3.easeLinear)
                    .attr("transform", "translate(" + x(previous_date_start) + ")")
                    .on("end", tick);

            }
        }
            //http://bl.ocks.org/atmccann/8966400

    },
    mounted (){
        this.renderChart();
    }
}

</script>

<style>
    text{
        font-size: 30px;
        font-family: Open Sans, sans-serif;
    }
    .line{
        stroke: green;
        fill : none;
        stroke-width: 4px;
    }
    .yearText{
        font-size: 170px;
        font-weight: 700;
        opacity: 0.25;
    }
    .ticker{
        font-weight: 20px
    }
</style>
