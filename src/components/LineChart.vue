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
import stockcsv from "../assets/stockdata.json"
//import brandData from "../assets/mobile_manufacture.json";
//import india from "../assets/images/india.png";
//var d3 = require('d3-scale','d3-array','d3-fetch','d3-selection','d3-timer','d3-color','d3-format','d3-ease','d3-interpolate','d3-axis','d3-selection-multi');


export default {
    name : "LineChart",
    data(){
        return{
            stockcsv
        }
    },
    methods : {
        renderChart : function(){
            //const tickDuration = 800
            //const top_n = 15;

            const height = 1650;
            const width = 3500;

            const margin = {
                top: 60,
                right: 220,
                bottom: 5,
                left: 450
            };

            var parseDate = d3.timeParse("%b %Y");

            /*const getImgUrl = function(imagename) {
                let result;
                try {
                    result = require("../assets/images/"+imagename+".png");
                }
                catch (e) {
                    result  = undefined;
                }
                return result;
            }*/

            //console.log(stockcsv);

            stockcsv.forEach(d => {
                d.price = isNaN(d.price) ? 0 : d.price,
                d.date = parseDate(d.date)
            });

            console.log(stockcsv);

            // Filter to one symbol; the S&P 500.
            var values = stockcsv.filter(function(d) {
                return d.symbol == "AMZN";
            });

            /*var msft = stockcsv.filter(function(d) {
                return d.symbol == "MSFT";
            });

            var ibm = stockcsv.filter(function(d) {
                return d.symbol == 'IBM';
            });*/

            var x = d3.scaleTime()
                        .domain(d3.extent(stockcsv, function(d) { return d.date; }))
                        .range([margin.left, width-margin.right]),
                y = d3.scaleLinear()
                        .domain([0, d3.max(values, function(d) { return d.price; })])
                        .range([height-margin.bottom-50, margin.top]);

            var xAxis = d3.axisBottom()
                        .scale(x)
                        .ticks(width > 500 ? 5:2);

            var yAxis = d3.axisLeft()
                        .scale(y)
                        .ticks(4);

            var line = d3.line()
                .x(function(d) { return x(d.date); })
                .y(function(d) { return y(d.price); });


            const svg = d3.select("#chart").append("svg")
                            .attr("width", width)
                            .attr("height", height)
                            .attr("class", "graph-svg-component");

            // Add the x-axis.
            svg.append('g')
                .attrs({
                    class: 'axis xAxis',
                    transform: `translate(0, ${height-margin.bottom-50})`
                })
                .call(xAxis)
                .selectAll('.tick line')
                .classed('origin', d => d == 0);

            // Add the y-axis.
            svg.append("g")
                .attrs({
                    class: 'axis yAxis',
                    transform: `translate(${margin.left},0)`
                })
                .call(yAxis);

            //var colors = d3.scaleOrdinal(d3.schemeCategory10);
            svg.selectAll('.stock')
                .data([values])
                .enter()
                .append('g')
                .attr('class', 'stock')
            
            var path = svg.selectAll(".stock").append("path")
                .attr("class", "line")
                .attr("d", function(d) { return line(d); })
                .style("stroke","red")
                .style("fill", "none");

            var totalLength = [path._groups[0][0].getTotalLength()];

            d3.select(path._groups[0][0])
                .attr("stroke-dasharray", totalLength[0] + " " + totalLength[0] ) 
                .attr("stroke-dashoffset", totalLength[0])
                .transition()
                .ease(d3.easeLinear)
                .duration(20000)
                .attr("stroke-dashoffset", 0);

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
