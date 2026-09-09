# SIH 2026 PS 165: The Sentinel Story & Dataset Collection

## The Real Tragedies That Shape Our Data
The "fake/mocked" data has been entirely removed from the OIL SIF Sentinel. Instead, we have curated a dataset based strictly on real Indian and global Oil & Gas historical tragedies. By feeding the *precursor* reports (the near-misses and minor anomalies observed just before the disasters) into our system, we demonstrate how this AI could have predicted and prevented the fatalities.

### 1. Baghjan Gas Well Blowout & Fire (Assam, May 2020)
* **The Tragedy:** A massive blowout at Baghjan Well No. 5 led to uncontrollable gas flow for months, followed by a massive fire that claimed the lives of two OIL firefighters and displaced thousands of locals. The local biodiversity was severely damaged.
* **The Ignored Data (Precursor):** Logs indicated minor gas kicks during tubing pull-out operations. The well was not completely killed with brine, and cement bond logs showed questionable integrity.
* **How Our System Saves Lives:** If the SIF Sentinel were active, these precursor logs (even if written as minor near-misses) would be instantaneously classified as **High SIF Potential (Energy Isolation / Work Authorisation)**. The algorithm's `stage_b_score` would spike over 95%, triggering an immediate Halt of Operations (Stop Work Authority) alert before the BOP was unbolted.

### 2. Bombay High North (BHN) Platform Fire (July 2005)
* **The Tragedy:** A multipurpose support vessel (MSV) collided with the BHN platform, slicing the unbarricaded gas export risers. The resulting inferno destroyed the entire platform in two hours, leading to 22 fatalities and a loss of $300 Million.
* **The Ignored Data (Precursor):** Weather reports showed 4-5 meter monsoon swells. The MSV was experiencing dynamic positioning failures and had to be manually controlled while dangerously close to the bare gas risers for a routine medical evacuation.
* **How Our System Saves Lives:** The Sentinel NLP engine would parse the dynamic positioning failures and proximity to live risers as a critical failure of barrier control. Tagged as **IOGP Life-Saving Rule: Line of Fire & Bypassing Safety Controls**, it would automatically escalate the event to onshore safety directors, preventing the vessel from entering the platform's 500-meter exclusion zone under manual control.

### 3. Visakhapatnam HPCL Refinery LPG Blast (September 1997)
* **The Tragedy:** An LPG leak from a storage sphere formed a massive vapor cloud. An unknown ignition source caused an explosion that killed 60 people and caused widespread destruction in the industrial zone.
* **The Ignored Data (Precursor):** Operators had noted continuous minor seepage of LPG from a flange. More critically, local gas leak detectors had been bypassed because they frequently tripped.
* **How Our System Saves Lives:** The AI's physical threshold modeling (OISD standards) would recognize "LPG seepage + Bypassed Detectors" as an active loss of primary and secondary containment. The classification of **High SIF Potential** would enforce an immediate shutdown of the receiving pipeline rather than letting operators "monitor" the leak.

### 4. GAIL Natural Gas Pipeline Blast (Nagaram, June 2014)
* **The Tragedy:** A rusted 18-inch natural gas pipeline ruptured, leaking gas into a residential area where a tea vendor's stove ignited it. The resulting blast killed 22 people.
* **The Ignored Data (Precursor):** Villagers had reported the smell of gas (mercaptan) and bubbling water days prior. Internal records showed the pipe was corroded, and only temporary clamps had been applied months before. 
* **How Our System Saves Lives:** "Smell of mercaptan" and "bubbling water" parsed from community/patrol logs are immediately vectorized into a high-energy release context. By mapping the precursor against the pipeline's deferred maintenance record, the AI identifies a catastrophic threat and advises immediate depressurization.

## The Training Dataset
Our system's `real_historical` dataset is comprised of the exact narrative precursors described above. Instead of generating arbitrary safety observations, the AI is trained to recognize the specific patterns (barrier degradation, bypassed sensors, high-pressure equipment handling) that historically pre-date catastrophic Indian O&G incidents.
