# HackMerlin Solver
---

## 🚀 How to Run

1. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your environment variables**  
   Create a `.env` file in the project root:
   ```env
   SESSION=your_hackmerlin_session_cookie
   CF_CLEARANCE=your_cloudflare_clearance_cookie
   DEEPSEEK_API_KEY=your_deepseek_api_key
   ```

3. **Run the program**
   ```bash
   python main.py
   ```

4. **Choose an option**
   - `1` → Enter password manually  
   - `2` → Auto-solver (recommended)  
   - `3` → Exit  

---

## 📂 Logs

- `logs/level_prompt_log.txt` → saves all questions/answers with Merlin  
- `logs/answer_log.txt` → saves all candidate guesses  

Logs reset when a level is solved.  

---

## 📊 Flowchart

Flowchart here:  
👉 [sample/hackmerlin_flow.pdf](sample/hackmerlin_flow.pdf)

---

## 🛠️ Project Structure

- **main.py** → Starts program, shows menu  
- **solver.py** → Auto-solver loop (questions → guesses → submit)  
- **agent.py** → Talks to Merlin + logs Q/A  
- **merlin_solver.py** → Creates candidate passwords  
- **submitter.py** → Submits guesses to API  
- **levels.py** → Saves solved levels  
- **instructions.py** → Question rules per level  
- **llm.py** → Connects to DeepSeek API  
- **config.py** → Loads .env variables  

---

