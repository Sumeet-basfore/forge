import { greet } from "../src/index.js";

function testGreet(): void {
  const result = greet("{{ project_name }}");
  if (result !== "Hello, {{ project_name }}!") {
    throw new Error(`Assertion failed: expected 'Hello, {{ project_name }}!', got '${result}'`);
  }
}

testGreet();
