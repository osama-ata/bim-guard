import { pathToFileURL } from 'node:url';

const statsMockUrl = 'data:text/javascript,' + encodeURIComponent(`
  const mockCalls = {
    showPanel: [],
    begin: [],
    end: [],
    remove: []
  };

  export const _mockCalls = mockCalls;

  export default class Stats {
    constructor() {
      this.dom = {
        style: {},
        remove: () => {
          mockCalls.remove.push([]);
        }
      };
    }
    showPanel(panel) {
      mockCalls.showPanel.push([panel]);
    }
    begin() {
      mockCalls.begin.push([]);
    }
    end() {
      mockCalls.end.push([]);
    }
  }
`);

export function resolve(specifier, context, nextResolve) {
  if (specifier === 'stats.js') {
    return {
      shortCircuit: true,
      url: statsMockUrl
    };
  }
  if (specifier === '@/types') {
    return {
      shortCircuit: true,
      url: 'data:text/javascript,export {}'
    };
  }
  return nextResolve(specifier, context);
}
