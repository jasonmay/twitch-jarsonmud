/* eslint-disable */

import {TimelineMax} from 'gsap';

const P_WIDTH = 100;
const P_HEIGHT = 40;
const P_OFFSET = 50;

const START_CELL_X = 2;
const START_CELL_Y = 2;

class Navigator {

    constructor(px, py) {
        // how many rooms wide, rooms long
        this.px = px;
        this.py = py;

        this.cx = START_CELL_X;
        this.cy = START_CELL_Y;

        this._moving = false;

        this.timeline = new TimelineMax();
    }

    _leftSide(x, y) {
        return P_WIDTH + x * P_WIDTH * 2 + (this.py - y - 1) * P_OFFSET * 2;
    }

    _topSide(x, y) {
        return P_HEIGHT + y * P_HEIGHT * 2;
    }

    _viewBoxLeft(x, y) {
        return this._leftSide(x, y) - (this._viewBoxWidth() - P_OFFSET - P_WIDTH) / 2;
    }

    _viewBoxTop(x, y) {
        return this._topSide(x, y) - ((this._viewBoxHeight() - P_HEIGHT) / 2);
    }

    _viewBoxWidth(x, y) {
        return P_WIDTH * 3;
    }

    _viewBoxHeight(x, y) {
        return this._viewBoxWidth(x, y) * this.aspectRatio;
    }


    drawRooms(svg) {
        const b = svg.getBoundingClientRect()
        console.log(b)
        this.aspectRatio = b.height / b.width;
        const tx = this.px;
        const ty = this.py;

        const vbx = this._viewBoxLeft(this.cx, this.cy);
        const vby = this._viewBoxTop(this.cx, this.cy);
        const vbw = this._viewBoxWidth(this.cx, this.cy);
        const vbh = this._viewBoxHeight(this.cx, this.cy);

        const viewBox = [vbx, vby, vbw, vbh].join(" ");

        svg.setAttribute("viewBox", viewBox);

        for (let y = 0; y < ty; y++) {
            for (let x = 0; x < tx; x++) {
                const pTop = P_HEIGHT + y * P_HEIGHT * 2
                const pLeft = P_WIDTH + x * P_WIDTH * 2 + (ty - y-1) * P_OFFSET * 2
                var points = [
                    [pLeft + P_OFFSET, pTop],
                    [pLeft + P_WIDTH + P_OFFSET, pTop],
                    [pLeft + P_WIDTH, pTop + P_HEIGHT],
                    [pLeft, pTop + P_HEIGHT],
                ];
                var pointsAsStrings = points.map(e => e.join(","));
                const polygon = document.createElementNS("http://www.w3.org/2000/svg", 'polygon');
                polygon.setAttribute("points", pointsAsStrings.join(" "));
                polygon.style = "stroke: black; fill: white;";

                let selectRoom = () => this.selectRoom(x, y);
                polygon.addEventListener("click", selectRoom);

                svg.appendChild(polygon);
            }
        }
    }

    isMoving() {
        return this._moving;
    }

    selectRoom(x, y) {
        console.log("selectRoom " + x + " " + y);
    }

    goDirection(svg, x, y) {
        const vbw = this._viewBoxWidth(this.cx + x, this.cy + y);
        const vbh = this._viewBoxHeight(this.cx + x, this.cy + y);
        const vbx = this._viewBoxLeft(this.cx + x, this.cy + y);
        const vby = this._viewBoxTop(this.cx + x, this.cy + y);

        const viewBox = [vbx, vby, vbw, vbh].join(" ");

        this._moving = true;
        console.log("before");
        this.timeline.to(
            svg, 0.3, {attr: { viewBox: viewBox }}
        ).eventCallback(
            "onComplete", (() => { this._moving = false; }).bind(this)
        );
        console.log("after");
        this.cx += x;
        this.cy += y;
    }
}

export default Navigator
