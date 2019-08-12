/* eslint-disable */

const P_WIDTH = 100;
const P_HEIGHT = 40;
const P_OFFSET = 50;

class Navigator {

    constructor(px, py) {
        // how many rooms wide, rooms long
        this.px = px;
        this.py = py;
    }

    _leftSide(x, y) {
        return P_WIDTH + x * P_WIDTH * 2 + (this.py - y - 1) * P_OFFSET * 2;
    }

    _topSide(x, y) {
        return P_HEIGHT + y * P_HEIGHT * 2;
    }

    drawRooms(svg) {
        const b = svg.getBoundingClientRect()
        console.log(b)
        const aspectRatio = b.height / b.width;
        const tx = this.px;
        const ty = this.py;

        const vpx = 1;
        const vpy = 2;

        const vbw = P_WIDTH * 3;
        const vbh = vbw * aspectRatio;
        const vbx = this._leftSide(vpx, vpy) - (vbw - P_OFFSET - P_WIDTH) / 2;
        const vby = this._topSide(vpx, vpy) - ((vbh - P_HEIGHT) / 2);

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

    selectRoom(x, y) {
        console.log("haha " + x + " " + y);
    }
}

export default Navigator
