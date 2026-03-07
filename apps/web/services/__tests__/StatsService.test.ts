import { test, describe } from "node:test";
import assert from "node:assert";

// @ts-ignore
import { _mockCalls } from "stats.js";
import { StatsService } from "../StatsService.ts";

describe("StatsService", () => {
    test("should initialize with default panel and styles", () => {
        // Clear previous calls
        _mockCalls.showPanel.length = 0;

        const service = new StatsService();
        const dom = service.getDom();

        assert.strictEqual(_mockCalls.showPanel.length, 1);
        assert.strictEqual(_mockCalls.showPanel[0][0], 0);

        assert.strictEqual(dom.style.position, "absolute");
        assert.strictEqual(dom.style.top, "0");
        assert.strictEqual(dom.style.left, "0");
    });

    test("begin() should call stats.begin()", () => {
        _mockCalls.begin.length = 0;
        const service = new StatsService();
        service.begin();
        assert.strictEqual(_mockCalls.begin.length, 1);
    });

    test("end() should call stats.end()", () => {
        _mockCalls.end.length = 0;
        const service = new StatsService();
        service.end();
        assert.strictEqual(_mockCalls.end.length, 1);
    });

    test("getDom() should return the stats DOM element", () => {
        const service = new StatsService();
        const dom = service.getDom();
        assert.ok(dom);
        assert.ok(dom.style);
    });

    test("dispose() should remove the DOM element", () => {
        _mockCalls.remove.length = 0;
        const service = new StatsService();
        service.dispose();
        assert.strictEqual(_mockCalls.remove.length, 1);
    });
});
