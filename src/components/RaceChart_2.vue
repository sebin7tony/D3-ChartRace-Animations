/* eslint-env browser */
<template>
    <div style="margin : 15px;">
        <h3 style="margin-left:450px;font-weight: bold;font-size: 90px;margin-bottom: 10px;margin-top:30px; ">
            US presidents with the highest approval rating in history(in %)
        </h3>
        <div id="chart">
        </div>
    </div>
</template>

<script>

import * as d3 from "d3";
import "d3-selection-multi";
import brandData from "../assets/approval_ratings_barchartrace.json";
//import brandData from "../assets/mobile_manufacture.json";
//import india from "../assets/images/india.png";
//var d3 = require('d3-scale','d3-array','d3-fetch','d3-selection','d3-timer','d3-color','d3-format','d3-ease','d3-interpolate','d3-axis','d3-selection-multi');


export default {
    name : "RaceChart",
    data(){
        return{
            brandData
        }
    },
    methods : {
        renderChart : function() {

            const tickDuration = 1500
            const top_n = 12;

            const height = 1650;
            const width = 3500;

            

            const halo = function(text, strokeWidth) {
                text.select(function() { return this.parentNode.insertBefore(this.cloneNode(true), this); })
                    .style({
                        fill: '#ffffff',
                        stroke: '#ffffff',
                        'stroke-width': strokeWidth,
                        'stroke-linejoin': 'round',
                        opacity: 1
                    }); 
            }

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

            const svg = d3.select("#chart").append("svg")
                            .attr("width", width)
                            .attr("height", height)
                            .attr("class", "graph-svg-component");


            const margin = {
                top: 60,
                right: 220,
                bottom: 5,
                left: 450
            };
                            
            /*svg.append("defs")
                .append("pattern")
                .attr("id", "venus")
                .attr('patternUnits', 'userSpaceOnUse')
                .attr("width", width)
                .attr("height", height)
                .append("image")
                .attr("xlink:href", getImgUrl())
                .attr("width", width)
                .attr("height", height);*/

            

            
            let barPadding = (height-(margin.bottom+margin.top))/(top_n*5);
            
            /*let title = svg.append('text')
                .attrs({
                    class: 'title',
                    y: 40,
                    x : margin.left
                })
                .html('18 years of Interbrand’s Top Global Brands (Brand value, $m)');*/
            
            /*let subTitle = svg.append('text')
                .attrs({
                class: 'subTitle',
                y: 55
                })
                .html('Brand value, $m');*/
            
            /*let caption = svg.append('text')
                .attrs({
                class: 'caption',
                x: width,
                y: height-5
                })
                .styles({
                'text-anchor': 'end'
                })
                .html('Source: Interbrand');*/
            let year = 60;

            /*let months = {};
            months[0] = "Jan";
            months[1] = "Feb";
            months[2] = "Mar";
            months[3] = "Apr";
            months[4] = "May";
            months[5] = "Jun";
            months[6] = "Jul";
            months[7] = "Aug";
            months[8] = "Sep";
            months[9] = "Oct";
            months[10] = "Nov";
            months[11] = "Dec";*/

            //caption;
            //title;
            //subTitle;

            
            brandData.forEach(d => {
                d.value = +d.value,
                d.lastValue = +d.lastValue,
                d.value = isNaN(d.value) ? 0 : d.value,
                d.year = +d.year,
                d.colour = d3.hsl(Math.random()*360,0.50,0.60)
                d.image = getImgUrl(d.name)
            });
            
            console.log(brandData);
            console.log("Execution");
            
            let yearSlice = brandData.filter(d => d.year == year && !isNaN(d.value))
                .sort((a,b) => b.value - a.value)
                .slice(0,top_n);

            console.log(yearSlice);
            
            yearSlice.forEach((d,i) => d.rank = i);
            
            let x = d3.scaleLinear()
                .domain([0, d3.max(yearSlice, d => d.value)])
                .range([margin.left, width-margin.right-110]);
            
            let y = d3.scaleLinear()
                .domain([top_n,0])
                .range([height-margin.bottom, margin.top]);


            /*svg.append("rect")
                .attr("x", x(0)+30)
                .attr("y", y(0)+30)
                .attr("width", width)
                .attr("height", height)
                .attr("fill", "url(#venus)");*/
            
            let xAxis = d3.axisTop()
                .scale(x)
                .ticks(width > 500 ? 5:2)
                .tickSize(-(height-margin.top-margin.bottom))
                .tickFormat(d => d3.format(',')(d));
            
            svg.append('g')
                .attrs({
                class: 'axis xAxis',
                transform: `translate(0, ${margin.top})`
                })
                .call(xAxis)
                .selectAll('.tick line')
                .classed('origin', d => d == 0);
            
            svg.selectAll('rect.bar')
                .data(yearSlice, d => d.name)
                .enter()
                .append('rect')
                .attrs({
                class: 'bar',
                x: x(0)+1,
                width: d => x(d.value)-x(0)-1,
                y: d => y(d.rank)+5,
                height: y(1)-y(0)-barPadding
                })
                .styles({
                fill: d => d.colour
                });
            
            svg.selectAll('text.label')
                .data(yearSlice, d => d.name)
                .enter()
                .append('text')
                .attrs({
                class: 'label',
                x: d => x(d.value)-10,
                y: d => y(d.rank)+5+((y(1)-y(0))/2)+1,
                'text-anchor': 'end'
                })
                .html(d => d.name);

            svg.selectAll('image.label')
                .data(yearSlice, d => d.name)
                .enter()
                .append('svg:image')
                .attrs({
                    class: 'barImage',
                    x: x(0)-170,
                    y: d => y(d.rank)+25+((y(1)-y(0))/2)-90,
                    'xlink:href': d => d.image,
                    'height' : '120px',
                    'width' : '120px'
                });
            
            svg.selectAll('text.valueLabel')
                .data(yearSlice, d => d.name)
                .enter()
                .append('text')
                .attrs({
                class: 'valueLabel',
                x: d => x(d.value)+5,
                y: d => y(d.rank)+5+((y(1)-y(0))/2)+1,
                })
                .text(d => d3.format('.2f')(d.lastValue));
            
            let yearText = svg.append('text')
                .attrs({
                class: 'yearText',
                x: width,
                y: height-60
                })
                .styles({
                'text-anchor': 'end'
                })
                .call(halo, 10);

                // .html(~~year)

            svg.append('text')
                .attrs({
                class: 'staticText',
                x: width,
                y: height-300
                })
                .styles({
                'text-anchor': 'end'
                })
                .html("Approval rating after")

            
            
            let ticker = d3.interval(e => {
            
                yearSlice = brandData.filter(d => d.year == year && !isNaN(d.value))
                .sort((a,b) => b.value - a.value)
                .slice(0,top_n);
                
                yearSlice.forEach((d,i) => d.rank = i);
                
                x.domain([0, d3.max(yearSlice, d => d.value)]);
                
                svg.select('.xAxis')
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .call(xAxis);
                
                let bars = svg.selectAll('.bar').data(yearSlice, d => d.name);
                
                bars
                .enter()
                .append('rect')
                .attrs({
                    class: d => `bar ${d.name.replace(/\s/g,'_')}`,
                    x: x(0)+1,
                    width: d => x(d.value)-x(0)-1,
                    y: d => y(top_n+1)+5,
                    height: y(1)-y(0)-barPadding
                })
                .styles({
                    fill: d => d.colour
                })
                .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attrs({
                    y: d => y(d.rank)+5
                    });
                
                bars
                .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attrs({
                    width: d => x(d.value)-x(0)-1,
                    y: d => y(d.rank)+5
                    });
                
                bars
                .exit()
                .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attrs({
                    width: d => x(d.value)-x(0)-1,
                    y: d => y(top_n+1)+5
                    })
                    .remove();
                
                let labels = svg.selectAll('.label').data(yearSlice, d => d.name);
                
                labels
                .enter()
                .append('text')
                .attrs({
                    class: 'label',
                    x: d => x(d.value)-10, 
                    y: d => y(top_n+1)+5+((y(1)-y(0))/2),
                    'text-anchor': 'end'
                })
                .html(d => d.name)    
                .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attrs({
                    y: d => y(d.rank)+5+((y(1)-y(0))/2)+1,
                    });
                
                labels
                .transition()
                .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attrs({
                    x: d => x(d.value)-10, 
                    y: d => y(d.rank)+5+((y(1)-y(0))/2)+1
                    });
                
                labels
                .exit()
                .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attrs({
                    x: d => x(d.value)-10, 
                    y: d => y(top_n+1)+5
                    })
                    .remove();

                let imageLabels = svg.selectAll('.barImage').data(yearSlice, d => d.name);
                
                imageLabels
                .enter()
                .append('svg:image')
                .attrs({
                    class: 'barImage',
                    x: x(0)-170,
                    y: d => y(d.rank)+25+((y(1)-y(0))/2)-90,
                    'xlink:href': d => d.image,
                    'height' : '120px',
                    'width' : '120px'
                })
                .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attrs({
                    y: d => y(d.rank)+25+((y(1)-y(0))/2)-90
                    });
                
                imageLabels
                .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attrs({
                    x:  x(0)-170,
                    y: d => y(d.rank)+25+((y(1)-y(0))/2)-90
                    });
                
                imageLabels
                .exit()
                .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attrs({
                    x:  x(0)-170,
                    y: d => y(top_n+1)+25
                    })
                    .remove();

                
                let valueLabels = svg.selectAll('.valueLabel').data(yearSlice, d => d.name);
                
                valueLabels
                .enter()
                .append('text')
                .attrs({
                    class: 'valueLabel',
                    x: d => x(d.value)+5,
                    y: d => y(top_n+1)+5,
                })
                .text(d => d3.format('.2f')(d.lastValue))
                .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attrs({
                    y: d => y(d.rank)+5+((y(1)-y(0))/2)+1
                    });
                
                valueLabels
                .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attrs({
                    x: d => x(d.value)+5,
                    y: d => y(d.rank)+5+((y(1)-y(0))/2)+1
                    })
                    .tween("text", function(d) {
                        let i = d3.interpolateNumber(d.lastValue, d.value);
                        return function(t) {
                            this.textContent = d3.format('.2f')(i(t));
                        };
                    });
                
                valueLabels
                .exit()
                .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attrs({
                    x: d => x(d.value)+5,
                    y: d => y(top_n+1)+5
                    })
                    .remove();
                
                yearText.html(~~year+" days");
                
                if(year == 1450) ticker.stop();
                year = d3.format('.1f')((+year) + 5);
            },tickDuration);

            return svg.node();
        }
    },
    mounted : function(){
        this.renderChart();
    }
}

</script>

<style>
text{
  font-size: 50px;
  font-family: Open Sans, sans-serif;
}
text.title{
  font-size: 40px;
  font-weight: 500;
}
text.subTitle{
  font-weight: 500;
  fill: #777777;
}
text.caption{
  font-weight: 400;
  font-size: 14px;
  fill: #777777;
}
text.label{
  font-weight: 100;
}
text.yearText{
  font-size: 240px;
  font-weight: 700;
  opacity: 0.25;
}
text.staticText{
    font-size: 100px;
    font-weight: 300;
    opacity: 0.50;
}

.tick text {
  fill: #777777;
}
.xAxis .tick:nth-child(2) text {
  text-anchor: start;
}
.tick line {
  shape-rendering: CrispEdges;
  stroke: #949393;
}
.tick line.origin{
  stroke: #797272;
}
path.domain{
  display: none;
}
/*.graph-svg-component {
 background-color : #f2f0f0;
}*/
</style>
