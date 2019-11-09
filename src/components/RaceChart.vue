<template>
    <div id="chart">
    </div>
</template>

<script>

import * as d3 from "d3";
import brandData from "../assets/csvjson.json";


export default {
    name : "RaceChart",
    data(){
        return{
            brandData
        }
    },
    methods : {
        renderChart : function() {

            const tickDuration = 333
            const top_n = 12;
            //var brandData = [];

            //console.log(csvData);

            /*d3.csv(csvData,function(data){
                brandData = data;
                console.log(JSON.stringify(data));
            });*/

            const height = 1500;
            const width = 1500;

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

            const svg = d3.select("#chart").append("svg")
                        .attr("width", height)
                        .attr("height", width)
            
            const margin = {
                top: 80,
                right: 0,
                bottom: 5,
                left: 0
            };

            let barPadding = (height-(margin.bottom+margin.top))/(top_n*5);

            let title = svg.append('text')
                .attr('class', 'title')
                .attr('y', 24)
                .html('18 years of Interbrand’s Top Global Brands');

            let subTitle = svg.append('text')
                .attr('class', 'subTitle')
                .attr('y', '55')
                .html('Brand value, $m');

            let caption = svg.append('text')
                .attr('class', 'caption')
                .attr('x', width)
                .attr('y', height-5)
                .append('style')
                .text("'text-anchor': 'end'")
                .html('Source: Interbrand');

            let year = 2000;
            caption;
            subTitle;
            title;

            brandData.forEach(d => {
                d.value = +d.value,
                d.lastValue = +d.lastValue,
                d.value = isNaN(d.value) ? 0 : d.value,
                d.year = +d.year,
                d.colour = d3.hsl(Math.random()*360,0.75,0.75)
            });

            let yearSlice = brandData.filter(d => d.year == year && !isNaN(d.value))
                .sort((a,b) => b.value - a.value)
                .slice(0,top_n);

            yearSlice.forEach((d,i) => d.rank = i);

            let x = d3.scaleLinear()
                .domain([0, d3.max(yearSlice, d => d.value)])
                .range([margin.left, width-margin.right-65]);

            let y = d3.scaleLinear()
                .domain([top_n, 0])
                .range([height-margin.bottom, margin.top]);

            let xAxis = d3.axisTop()
                .scale(x)
                .ticks(width > 500 ? 5:2)
                .tickSize(-(height-margin.top-margin.bottom))
                .tickFormat(d => d3.format(',')(d));

            svg.append('g')
                .attr('class' , 'axis xAxis')
                .attr('transform' , `translate(0, ${margin.top})`)
                .call(xAxis)
                    .selectAll('.tick line')
                    .classed('origin', d => d == 0);

            svg.selectAll('rect.bar')
                .data(yearSlice, d => d.name)
                .enter()
                .append('rect')
                .attr('class' , 'bar')
                .attr('x' , x(0)+1)
                .attr('width' , d => x(d.value)-x(0)-1)
                .attr('y' , d => y(d.rank)+5)
                .attr('height' , y(1)-y(0)-barPadding)
                .style({
                    fill: d => d.colour
                });

            svg.selectAll('text.label')
                .data(yearSlice, d => d.name)
                .enter()
                .append('text')
                .attr('class' , 'label')
                .attr('x' , d => x(d.value)-8)
                .attr('y' , d => y(d.rank)+5+((y(1)-y(0))/2)+1)
                .attr('text-anchor' , 'end')
                .html(d => d.name);

            svg.selectAll('text.valueLabel')
                .data(yearSlice, d => d.name)
                .enter()
                .append('text')
                .attr('class' , 'valueLabel')
                .attr('x' , d => x(d.value)+5)
                .attr('y' , d => y(d.rank)+5+((y(1)-y(0))/2)+1)
                .text(d => d3.format(',.0f')(d.lastValue));

            let yearText = svg.append('text')
                .attr('class' , 'yearText')
                .attr('x' , width-margin.right)
                .attr('y' , height-25)
                .html(~~year)
                .call(halo, 10)
                .style({
                    'text-anchor': 'end'
                });

            let ticker = d3.interval(e => {

                e;
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
                    .attr('class' , d => `bar ${d.name.replace(/\s/g,'_')}`)
                    .attr('x' , x(0)+1)
                    .attr('width' , d => x(d.value)-x(0)-1)
                    .attr('y' , d => {
                            d;
                            return y(top_n+1)+5;
                    })
                    .attr('height' , y(1)-y(0)-barPadding)
                    .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attr('y' , d => y(d.rank)+5);

                bars
                    .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attr('width' , d => x(d.value)-x(0)-1)
                    .attr('y' , d => y(d.rank)+5);

                bars
                    .exit()
                    .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attr('width' , d => x(d.value)-x(0)-1)
                    .attr('y' , d => {
                            d;
                            return y(top_n+1)+5
                    })
                    .remove();

                let labels = svg.selectAll('.label').data(yearSlice, d => d.name);

                labels
                    .enter()
                    .append('text')
                    .attr('class' , 'label')
                    .attr('x' , d => x(d.value)-8)
                    .attr('y' , d => {
                        d;
                        return y(top_n+1)+5+((y(1)-y(0))/2)
                    })
                    .attr('text-anchor' , 'end')
                    .html(d => d.name)    
                    .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attr('y' , d => y(d.rank)+5+((y(1)-y(0))/2)+1,);

                labels
                    .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attr('x' , d => x(d.value)-8)
                    .attr('y' , d => y(d.rank)+5+((y(1)-y(0))/2)+1);

                labels
                    .exit()
                    .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attr('x' , d => x(d.value)-8)
                    .attr('y' , d => {
                            d;
                            return y(top_n+1)+5
                    })
                    .remove();

                let valueLabels = svg.selectAll('.valueLabel').data(yearSlice, d => d.name);

                valueLabels
                    .enter()
                    .append('text')
                    .attr('class' , 'valueLabel')
                    .attr('x' , d => x(d.value)+5)
                    .attr('y' , d => {
                        d;
                        return y(top_n+1)+5
                    })
                    .text(d => d3.format(',.0f')(d.lastValue))
                    .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attr('y' , d => y(d.rank)+5+((y(1)-y(0))/2)+1);

                valueLabels
                    .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attr('x' , d => x(d.value)+5)
                    .attr('y' , d => y(d.rank)+5+((y(1)-y(0))/2)+1)
                    .tween("text", function(d) {
                        let i = d3.interpolateRound(d.lastValue, d.value);
                        return function(t) {
                        this.textContent = d3.format(',')(i(t));
                        };
                    });

                valueLabels
                    .exit()
                    .transition()
                    .duration(tickDuration)
                    .ease(d3.easeLinear)
                    .attr('x' , d => x(d.value)+5)
                    .attr('y' , d => {  
                            d;
                            return y(top_n+1)+5;
                    })
                    .remove();

        
                yearText;

                if(year == 2018) ticker.stop();
                year = d3.format('.1f')((+year) + 0.1);
            },tickDuration);
        }
    },
    mounted : function(){
        this.renderChart();
    }
}



</script>

<style>
text{
  font-size: 16px;
  font-family: Open Sans, sans-serif;
}
text.title{
  font-size: 24px;
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
  font-weight: 600;
}
text.yearText{
  font-size: 64px;
  font-weight: 700;
  opacity: 0.25;
}
.tick text {
  fill: #777777;
}
.xAxis .tick:nth-child(2) text {
  text-anchor: start;
}
.tick line {
  shape-rendering: CrispEdges;
  stroke: #dddddd;
}
.tick line.origin{
  stroke: #aaaaaa;
}
path.domain{
  display: none;
}
</style>
