import sqlite3

def init_db():
    conn = sqlite3.connect('project_parts.db')
    cursor = conn.cursor()
    # Table to store the generated codes and their metadata
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            category TEXT,
            type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def get_next_sequence(conn, prefix):
    cursor = conn.cursor()
    # Find the highest existing number for this specific prefix
    cursor.execute("SELECT code FROM inventory WHERE code LIKE ? ORDER BY code DESC LIMIT 1", (f"{prefix}%",))
    last_code = cursor.fetchone()
    
    if last_code:
        # Assumes a fixed length for consistency, e.g., 00001
        last_num = int(last_code[0][1:]) 
        return str(last_num + 1).zfill(5)
    else:
        return "00001"

def generate_code(conn):
    print("\n--- Project Code Generator ---")
    choice = input("Select category: [P]art or [A]ssembly? ").strip().upper()

    if choice == 'P':
        print("Types: [1] Block, [2] Bar, [3] Sheet, [4] Machine Element")
        t_choice = input("Select type: ")
        mapping = {"1": "Block", "2": "Bar", "3": "Sheet", "4": "Machine Element"}
        
        if t_choice in mapping:
            prefix = t_choice
            cat_label = "Part"
            type_label = mapping[t_choice]
        else:
            print("Invalid type.")
            return

    elif choice == 'A':
        print("Types: [0] Main Assembly, [9] Sub-Assembly")
        t_choice = input("Select type: ")
        mapping = {"0": "Main Assembly", "9": "Sub-Assembly"}
        
        if t_choice in mapping:
            prefix = t_choice
            cat_label = "Assembly"
            type_label = mapping[t_choice]
        else:
            print("Invalid type.")
            return
    else:
        print("Invalid selection.")
        return

    # Generate and save
    suffix = get_next_sequence(conn, prefix)
    final_code = f"{prefix}{suffix}"
    
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (code, category, type) VALUES (?, ?, ?)", 
                       (final_code, cat_label, type_label))
        conn.commit()
        print(f"\nSuccessfully generated and stored: {final_code} ({type_label})")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def main():
    db_conn = init_db()
    try:
        while True:
            generate_code(db_conn)
            if input("\nGenerate another? (y/n): ").lower() != 'y':
                break
    finally:
        db_conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()
