//
// PieChart
//
// CreativeCommons Attribution-ShareAlike
// http://creativecommons.org/licenses/by-sa/2.5/
//
// 2011 Elisabeth Robson
//
// expects an object with one or more of these:
// includeLabels - boolean, determines whether to include the specified labels
//	when drawing the chart. If false, the labels are stored in the pie chart
//	but not drawn by default. You can draw a label for a segment with 
//	the drawLabel method.
// data - array of data items. Should be positive integer adding up to 360.
// labels - array of (string) labels. Should have at least as many items as data.
// colors - two D array of (string) colors. First is used to draw, second to draw
//	a selected segment.
//
var startAngleBuffer = 0; // value in degrees
var rotationIncrement = 7.5; // value in degrees
var spinDuration = 10000; // value in milliseconds

function Wheel(id, o)
{

    this.includeLabels = false;
    if (o.includeLabels === undefined)
    {
            this.includeLabels = false;
    }
    else 
    {
        this.includeLabels = o.includeLabels;
    }
    
    this.data = o.data ? o.data : [30, 70, 45, 65, 20, 130]; // in degrees
    this.labels = o.labels ? o.labels : ["First", "Second", "Third", "Fourth", "Fifth", "Sixth"];
    this.colors = o.colors ? o.colors : [
            ["#bbddb3", "#1d8e04"], // green
            ["#e2f5b4", "#9edd08"], // yellow green
            ["#fdfbb4", "#faf406"], // yellow
            ["#fbd4b7", "#f2700f"], // orange
            ["#f8bdb4", "#ea2507"], // red
            ["#e2bcbd", "#9e2126"]  // purple
    ];

    this.canvas = document.getElementById(id);
}


Wheel.prototype = {
    
    setLabels: function(labelsParam)
    {
        this.labels = labelsParam;
    },
    
    spin: function(gameController){
        var that = this;
        this.setDeceleratingTimeout(function(){that.rotate();}, 10, spinDuration, gameController);
    },

    setDeceleratingTimeout: function (callback, factor, times, gameController)
    {
        var self = this;
        var internalCallback = function(tick, counter) {
            return function() {

                tick = tick - tick/5;
                if (tick >= 1) {;
                    window.setTimeout(internalCallback, ++counter * factor);
                    callback();
                    console.log("tick " + tick);
                }
                else
                {
                    console.log("highlight");
                    self.draw(startAngleBuffer, true, gameController);
                }
            }
        }(times, 0);

        window.setTimeout(internalCallback, factor);
    },

    rotate: function() {
        startAngleBuffer += rotationIncrement;
        startAngleBuffer = startAngleBuffer % 360;
        this.draw(startAngleBuffer, false);
    },

    select: function(segment) {
            var self = this;
            var context = this.canvas.getContext("2d");
            this.drawSegment(this.canvas, context, segment, self.data[segment], true, self.includeLabels);
    },

    draw: function(startingRotationDegrees, highlight, gameController) {
            var self = this;

            var highlightIndex;
            if (highlight === true)
            {
                highlightIndex = (12 - Math.ceil((startingRotationDegrees % 360)/30))%12;
                console.log("startAngleBuffer: " + startingRotationDegrees);
                console.log("hightlightIndex: " + highlightIndex);
                console.log(self.labels[highlightIndex]); 

                gameController.processWheelCategory(self.labels[highlightIndex]);
            }

            var context = this.canvas.getContext("2d");
            var highlightSegment = false;
            for (var i = 0; i < this.data.length; i++) {
                if (highlight === true && i === highlightIndex)
                {
                    highlightSegment = true;
                }
                else
                {
                    highlightSegment = false;
                }

                this.drawSegment(this.canvas, context, i, this.data[i], highlightSegment, this.includeLabels);

            }
    },

    drawSegment: function(canvas, context, i, size, isSelected, includeLabels) {
            var self = this;
            context.save();
            var centerX = Math.floor(canvas.width / 2);
            var centerY = Math.floor(canvas.height / 2);
            radius = Math.floor(canvas.width / 2);

            var startingAngle = self.degreesToRadians(self.sumTo(self.data, i) + startAngleBuffer);
            var arcSize = self.degreesToRadians(size);
            var endingAngle = startingAngle + arcSize;

            context.beginPath();
            context.moveTo(centerX, centerY);
            context.arc(centerX, centerY, radius, startingAngle, endingAngle, false);
            context.closePath();

            isSelected ? 
                    context.fillStyle = self.colors[i][1] :
                    context.fillStyle = self.colors[i][0];

            context.fill();
            context.restore();

            if (includeLabels && (self.labels.length > i)) {
                    self.drawSegmentLabel(canvas, context, i, isSelected);
            }
    },

    drawSegmentLabel: function(canvas, context, i, isSelected) {
            var self = this;
            context.save();
            var x = Math.floor(canvas.width / 2);
            var y = Math.floor(canvas.height / 2);
            var angle;
            var angleD = self.sumTo(self.data, i);

            // var flip = (angleD < 90 || angleD > 270) ? false : true;
            var flip = false;  // Jason - don't flip the label

            context.translate(x, y);
            if (flip) {
                    angleD = angleD-180;
                    context.textAlign = "left";
                    angle = self.degreesToRadians(angleD + startAngleBuffer);
                    context.rotate(angle);
                    context.translate(-(x + (canvas.width * 0.5))+15, -(canvas.height * 0.05)-10);
            }
            else {
                    context.textAlign = "right";
                    angle = self.degreesToRadians(angleD + startAngleBuffer);
                    context.rotate(angle);
            }
            //context.textAlign = "right";
            // var fontSize = Math.floor(canvas.height / 25);
            var fontSize = Math.floor(canvas.height / 35); // Jason - reduced font size to fit
            context.font = fontSize + "pt Helvetica";

            var dx = Math.floor(canvas.width * 0.5) - 10;
            var dy = Math.floor(canvas.height * 0.05);
            context.fillText(self.labels[i], dx, dy);

            context.restore();
    },

    drawLabel: function(i) {
            var self = this;
            var context = this.canvas.getContext("2d");
            var size = self.data[i];

            self.drawSegmentLabel(this.canvas, context, i, size, false);
    },

    // helper functions
    degreesToRadians: function(degrees) {
            return (degrees * Math.PI)/180;
    },

    sumTo: function(a, i) {
            var sum = 0;
            for (var j = 0; j < i; j++) {
                    sum += a[j];
            }
            return sum;
    }
        
};