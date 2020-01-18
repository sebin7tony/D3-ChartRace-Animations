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
import stockdata from "../assets/approval_ratings.json"
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
            
            var parseDate = d3.timeParse("%Y-%m-%d");
            stockdata.forEach(d => {
                d.days = +d.days,
                d.approve_estimate = +d.approve_estimate
                d.date = parseDate(d.date)
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
            getImgUrl("")

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

            // Data preparation stage
            var trump_values = stockdata.filter(function(d) {
                return d.president == "Donald Trump";
            });

            var obama_values = stockdata.filter(function(d) {
                return d.president == "Barack Obama";
            });

            var bush_values = stockdata.filter(function(d) {
                return d.president == "George W. Bush";
            });

            var chart_data = [trump_values,obama_values,bush_values]

            for(var f=0;f<chart_data.length;f++){
                console.log(chart_data[f])
            }

            let xAxis_data = "days";
            let yAxis_data = "approve_estimate";
            let image_name = "president"

            // Common code begins here

            for(let values of chart_data){
                values.sort((a, b) => (a[xAxis_data] > b[xAxis_data]) ? 1 : -1);
            }    

            var limit = 60;
            var counter = -1;
            var data_reduction_factor = 3/5;
            
            var sliced_chart_data = [];
            for(let values of chart_data){
                let data = values.slice(0,limit)
                sliced_chart_data.push(data);
            }

            var margin = {top: 300, right: 40, bottom: 20, left: 80},
                width = 3600 - margin.right,
                height = (window.innerHeight/2+300) ;
            
            var x = d3.scaleLinear()
                .domain(d3.extent(sliced_chart_data[0], function(d) { return d[xAxis_data]; }))
                .range([0, width]);

            var y = window.y = d3.scaleLinear()
                .range([height, 0]);

            var line = d3.line()
                .curve(d3.curveBasis)
                .x(function(d, i) { 
                    return x(d[xAxis_data]); })
                .y(function(d, i) { 
                    return y(d[yAxis_data]); 
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

            var XaxisLabel = svg.append("text")
                    .data(sliced_chart_data[0])
                    .attrs({
                        class: 'XaxisLabel',
                        x: width-800,
                        y: height-100
                    })
                    .style('text-anchor', 'start')

            var approval_label = svg.append("text")
                    .attrs({
                        class: 'approvalLabel',
                        x: width-800,
                        y: height-270
                    })
                    .style('text-anchor', 'start')


            var image = [],name = [],path =[], value =[]; 

            for(var i=0;i<sliced_chart_data.length;i++){
                // Clipping start here
                path[i] = svg.append("g")
                    .attr("class", "path container")
                    .attr("clip-path", "url(#clip)")
                .append("path")
                    .data(sliced_chart_data[i])
                    .attr("class", "line"+i);

                // Appending various elements to svg
                image[i] = svg.append("svg:image")
                    .data(sliced_chart_data[i])
                    .attr('x', width-500)
                    .attr('y', i*300)
                    .attr('width', 280)
                    .attr('height', 280)
                    //.attr("transform", "translate(" + 800 +", " + y(2) + ")")
                    .attr("xlink:href", getImgUrl(sliced_chart_data[i][0][image_name]))
                
                name[i] = svg.append("text")
                    .data(sliced_chart_data[i])
                    .attr('class','ticker')
                    .attr('dx', 8)
                    .attr('dy', 3)
                    .attr("transform", "translate(" + (width - margin.left - margin.right) +", " + y(0) + ")")
                    .style('text-anchor', 'start')

                value[i] = svg.append("text")
                    .data(sliced_chart_data[i])
                    .attr('class','imgLabel')
                    .attr('x', width-220)
                    .attr('y', (2*i+1)*150+(i*20))
                    //.attr("transform", "translate(" + (width - margin.left - margin.right) +", " + y(0) + ")")
                    .style('text-anchor', 'start')
            }

            console.log(image)

            // -------------------------------------------
            // Logic for event addition
            // -------------------------------------------

            var tipList = []
            
            for(var k=0;k<event_lists.length;k++){
                var tip = svg.append("svg:image")
                    .data([event_lists[k]])
                    //.attr('dx', 0)
                    //.attr('dy', 0)
                    .attr('width', 1000)
                    .attr('height', 1000)
                    .attr("transform", "translate(" + -200 +", " + y(900) + ")")
                    .attr("xlink:href", getImgUrl(event_lists[k]['tooltip']));
                tipList.push(tip);
            }

            // -------------------------------------------
            // Logic for dashboard
            // -------------------------------------------



            // ----------------------------------------
            // declarations for tick function
            // ----------------------------------------            
            var line_chart_data = [];
            
            //lineData.push(data[0]);
            var duration_speed = 50;

            tick();

            function tick() {   

                counter = counter+1;
                var previous_date_start = sliced_chart_data[0][0][xAxis_data];

                // ----------------------------------------
                // resetting domain
                // ---------------------------------------- 
                if(chart_data[0].length > counter){
                    for(var i=0;i<sliced_chart_data.length;i++){
                        sliced_chart_data[i] = sliced_chart_data[i].slice(1-sliced_chart_data[i].length).concat(chart_data[i][limit+counter]);
                        line_chart_data[i] = sliced_chart_data[i].slice(0,data_reduction_factor*limit);
                    }
                    duration_speed = 450;
                }
                
                
                x.domain(d3.extent(sliced_chart_data[0], function(d) { return d[xAxis_data]; }));
                y.domain([30, 90]);

                
                // ----------------------------------------
                // redrawing line
                // ---------------------------------------- 
                for(i=0;i<line_chart_data.length;i++){
                    svg.select(".line"+i)
                        .attr("d", line(line_chart_data[i]))
                        .transition()
                        .ease(d3.easeLinear)
                        .attr("transform", null);
                }

                // slide the x-axis left
                xaxis.transition()
                    .duration(duration_speed)
                    .ease(d3.easeLinear)
                    .call(x.axis);

                yaxis.call(y.axis);
                
                // ----------------------------------------
                // elements animation
                // ---------------------------------------- 
                /*XaxisLabel.text(d =>{
                    return d3.timeFormat("%Y %b")(line_chart_data[0][line_chart_data[0].length-1][xAxis_data])
                });*/

                approval_label.html("Approval ratings after");

                XaxisLabel.text(d =>{
                    return line_chart_data[0][line_chart_data[0].length-1][xAxis_data]+" days"
                });
                
                for(i=0;i<line_chart_data.length;i++){
                    
                    name[i].text(d =>{
                        return d["president"]+" ("+d3.format('.2f')(line_chart_data[i][line_chart_data[i].length-1][yAxis_data])+")"
                        })
                        .transition()
                        .duration(100)
                        .attr("transform", function(d) { 
                            return "translate(" + x(line_chart_data[i][line_chart_data[i].length-2][xAxis_data]) +", " + y(line_chart_data[i][line_chart_data[i].length-1][yAxis_data]) + ")"});

                    value[i].text(d =>{
                        return d3.format('.2f')(line_chart_data[i][line_chart_data[i].length-1][yAxis_data])
                        })
                        /*.transition()
                        .duration(100)
                        .attr("transform", function(d) { 
                            return "translate(" + x(line_chart_data[i][line_chart_data[i].length-2][xAxis_data]) +", " + y(line_chart_data[i][line_chart_data[i].length-1][yAxis_data]-1) + ")"});*/

                    /*image[i].transition()
                        .duration(10)
                        .attr("transform", function(d) { 
                            return "translate(" + x(line_chart_data[i][line_chart_data[i].length-2][xAxis_data])+5 +", " + y(line_chart_data[i][line_chart_data[i].length-1][yAxis_data]+7) + ")"
                        });*/

                    }

                     // ----------------------------------------
                    // Path transition
                    // ---------------------------------------- 
                    path[0].transition()
                        .duration(duration_speed)
                        .ease(d3.easeLinear)
                        .attr("transform", "translate(" + x(previous_date_start) + ")");

                    path[1].transition()
                        .duration(duration_speed)
                        .ease(d3.easeLinear)
                        .attr("transform", "translate(" + x(previous_date_start) + ")")
                        .on("end", tick);

                    path[2].transition()
                        .duration(duration_speed)
                        .ease(d3.easeLinear)
                        .attr("transform", "translate(" + x(previous_date_start) + ")")
                

                // Tooltip animation

                for(i=0;i<tipList.length;i++){
                        
                    //console.log(tipList[0]);
                    tipList[i].transition()
                        .duration(duration_speed)
                        .ease(d3.easeLinear)
                        .attr("transform", function(d) { 
                            let xValue = x(d[xAxis_data]);
                            let yValue = d[xAxis_data] < line_chart_data[0][line_chart_data[0].length-1][xAxis_data] ? y(d[yAxis_data]+20) : -1000;
                            return "translate(" + xValue +", " + yValue + ")"
                        });
                }
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
        font-size: 50px;
        font-family: "Times New Roman", Times, serif;;
    }
    .line0{
        stroke: #ff471a;
        fill : none;
        stroke-width: 10px;
    }

    .line1{
        stroke: #3366ff;
        fill : none;
        stroke-width: 10px;
    }

    .line2{
        stroke: #ff8c1a;   
        fill : none;
        stroke-width: 10px;
    }

    .XaxisLabel{
        font-size: 170px;
        font-weight: 700;
        opacity: 0.25;
    }
    .approvalLabel{
        font-size: 80px;
        font-weight: 700;
        opacity: 0.25;
    }

    .ticker{
        font-weight: 20px
    }
    .imgLabel{
        font-size: 100px;
        font-weight: 700;
        opacity: 0.50;
    }
</style>
