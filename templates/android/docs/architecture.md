# Architecture: {{ project_name }}

## Purpose
<Describe what this project does and the problem it solves.>

## System Overview
<Describe the high-level Android application architecture, activities, services, and boundaries.>

## Key Modules
- `app/`: Primary application module.
- `app/src/main/AndroidManifest.xml`: Application manifest and permission declarations.
- `build.gradle.kts` & `settings.gradle.kts`: Kotlin DSL Gradle build scripts. Note: run `gradle wrapper` to generate local `gradlew` binaries if needed.

## Data Flow & State Management
<Describe how data flows through the application, UI state, and lifecycle handling.>

## Engineering Invariants
<List critical non-negotiable architectural or domain rules.>
