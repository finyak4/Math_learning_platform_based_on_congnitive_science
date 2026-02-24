🧠 [Project Name]: A Cognitive-Science-Based Learning Platform
📖 About The Project
[Project Name] is an open-source learning management system (LMS) and quiz platform built on the principles of cognitive psychology, specifically drawing from the book Make It Stick: The Science of Successful Learning.

Unlike traditional learning platforms that rely on passive video consumption and multiple-choice recognition, this platform is engineered to create desirable difficulties. By forcing learners to actively retrieve information, explain concepts in their own words, and tackle interleaved problem sets, the platform ensures long-term retention and deeper conceptual mastery.

Currently, the platform features curriculums for advanced mathematics (e.g., Gilbert Strang's Introduction to Linear Algebra, Probability, and Combinatorics).

🔬 The Cognitive Science Behind the Platform
Most traditional study methods (rereading, highlighting, massed practice/cramming) create an "Illusion of Competence." You feel like you know the material because it looks familiar, but you cannot recall it when tested.

This platform combats the forgetting curve by hardcoding the following evidence-based learning strategies into its architecture:

1. Retrieval Practice (Active Recall)
The Science: Pulling information out of your brain is far more effective for long-term memory than cramming information in.

Platform Implementation: The platform minimizes multiple-choice questions. Instead, it uses Automated Fill-in-the-Blank and Short Answer formats. The user must generate the answer from scratch, strengthening the neural pathways associated with that memory.

2. Elaboration
The Science: Learning is most robust when you can connect new knowledge to what you already know and explain it in your own words.

Platform Implementation: We utilize Self-Evaluated Quizzes focusing on "Story Proofs" and conceptual explanations (e.g., "Explain the President Identity using a team selection story"). Users type their explanations and grade themselves against a model answer, focusing on the why rather than just the what.

3. Interleaving
The Science: "Blocked practice" (doing 20 counting problems, then 20 probability problems) is less effective than "Interleaved practice" (mixing them up). Interleaving forces the brain to first identify which strategy to use before applying it.

Platform Implementation: The Revision Quizzes intentionally mix topics from different chapters and domains, simulating real-world problem-solving where the context is not pre-packaged.

4. Desirable Difficulty
The Science: Learning should feel a bit frustrating. The harder your brain works to retrieve a memory, the more thoroughly the memory is reconsolidated and strengthened.

Platform Implementation: The platform does not give immediate hints and requires precise terminology, ensuring the learner actually knows the material rather than just recognizing a familiar shape.

✨ Key Features
Dual-Evaluation System:

Automated Evaluation: For exact facts, formulas, and calculations (handles multiple accepted variations of an answer).

Self-Evaluation: For deep conceptual proofs and narrative explanations where automated grading falls short.

Granular Subject Tagging: Questions are tagged by Domain (e.g., Linear Algebra), Subject, and Topic to allow for targeted revision sets.

Secure Authentication: Integrated with Django AllAuth, allowing for secure local accounts and safe OAuth (Social) logins while preventing account hijacking.

Mathematical Rendering: Support for complex mathematical formulas and vector notations.

🛠️ Built With
Backend: Django (Python)

Authentication: Django AllAuth

Database: PostgreSQL 
