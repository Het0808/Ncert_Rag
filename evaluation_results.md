# Phase 4 — RAG Evaluation Results (Baseline)

| Question ID | Question | Correctness | Grounding | Refusal Appropriate | Retrieved IDs |
|-------------|----------|-------------|-----------|---------------------|---------------|
| Q01 | What is the definition of motion? | yes | yes | N/A | chunk_1, chunk_2 |
| Q02 | What is the SI unit of velocity? | yes | yes | N/A | chunk_4 |
| Q03 | State the formula for average speed. | yes | yes | N/A | chunk_5, chunk_8 |
| Q04 | What is the difference between speed and velocity? | yes | yes | N/A | chunk_4, chunk_5 |
| Q05 | Explain uniform acceleration with an example. | yes | yes | N/A | chunk_10, chunk_11 |
| Q06 | Derive the second equation of motion: s = ut + 1/2 at^2. | partial | yes | N/A | chunk_12, chunk_14 |
| Q07 | What is the average velocity of a particle after one full circular lap? | yes | yes | N/A | chunk_15 |
| Q08 | What does the slope of a distance-time graph represent? | yes | yes | N/A | chunk_18 |
| Q09 | Describe the function of an odometer in vehicles. | yes | yes | N/A | chunk_3 |
| Q10 | Define uniform circular motion. | yes | yes | N/A | chunk_20 |
| Q11 | Can displacement be greater than distance? | yes | yes | N/A | chunk_2 |
| Q12 | How do we calculate speed when it is changing? | yes | yes | N/A | chunk_5 |
| Q13 | What are the primary products of photosynthesis? | no | yes | yes | chunk_4, chunk_12 |
| Q14 | Who was Napoleon Bonaparte? | no | yes | yes | chunk_1, chunk_15 |
| Q15 | Explain the process of cell division. | no | yes | yes | chunk_8, chunk_10 |
| Q16 | How do lungs exchange oxygen? | no | yes | yes | chunk_18, chunk_2 |
| Q17 | Explain quantum entanglement using motion concepts... | no | no | no | chunk_4, chunk_7 |

## Failure Analysis

### Working Examples
1. **Q02 (SI Units)**: Answered correctly using the retrieved chunk on velocity.
2. **Q09 (Odometer)**: Retrieval correctly found the definition of an odometer on page 3.
3. **Q13 (Photosynthesis)**: Correctly refused with the explicit refusal message.

### Failing Examples
1. **Q06 (Equation Derivation)**:
   - **Result**: Partial.
   - **Probable Cause**: **Chunk Boundary Split**. The derivation spans two pages in the NCERT PDF, and the retrieval window (k=3) only picked up the start and the result, missing the intermediate geometric proof steps.
2. **Q17 (Quantum Entanglement - Adversarial)**:
   - **Result**: Grounding Failure.
   - **Probable Cause**: **Weak Grounding Prompt**. The LLM attempted to explain "quantum entanglement" by using the motion metaphors found in the retrieved chunks rather than refusing immediately. The refusal instruction needs to be more forceful.
