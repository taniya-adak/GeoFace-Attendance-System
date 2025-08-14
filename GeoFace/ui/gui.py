from os import name
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import face_recognition
from ui.styles import Colors, Fonts, configure_styles
from modules.face_recognition import recognize_face
from modules.database import add_attendance_record, get_all_records

class GeoFaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GeoFace Attendance System")
        self.root.geometry("900x700")
        self.root.configure(bg=Colors.BACKGROUND)
        
        # Initialize styles
        configure_styles()
        
        # Camera setup
        self.cap = None
        self.known_faces, self.known_names = recognize_face()
        
        # UI Structure
        self.create_header()
        self.create_camera_section()
        self.create_attendance_log()
        self.create_footer()
        
    def create_header(self):
        """Top header with title and buttons"""
        header = ttk.Frame(self.root)
        header.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(
            header,
            text="GeoFace Attendance",
            font=Fonts.TITLE,
            foreground=Colors.PRIMARY
        ).pack(side=tk.LEFT)
        
        btn_frame = ttk.Frame(header)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            btn_frame,
            text="Start Camera",
            command=self.start_camera
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Mark Attendance (A)",
            command=self.mark_attendance
        ).pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(
            header,
            text="Camera: OFF",
            foreground=Colors.TEXT_LIGHT
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)
    
    def create_camera_section(self):
        """Live camera feed display"""
        self.camera_frame = ttk.LabelFrame
        self.root,
        text="Live Camera Feed",
        padding=(10, 5)
        self.camera_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.camera_label = ttk.Label(self.camera_frame)
        self.camera_label.pack()
    
    def create_attendance_log(self):
        """Scrollable attendance log"""
        log_frame = ttk.LabelFrame(
            self.root,
            text="Attendance Records",
            padding=(10, 5))
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Treeview (table)
        self.log_table = ttk.Treeview(
            log_frame,
            columns=("id", "name", "time", "location"),
            show="headings",
            height=8
        )
        
        # Configure columns
        self.log_table.heading("id", text="ID")
        self.log_table.heading("name", text="Name")
        self.log_table.heading("time", text="Time")
        self.log_table.heading("location", text="Location")
        
        self.log_table.column("id", width=50, anchor="center")
        self.log_table.column("name", width=150)
        self.log_table.column("time", width=120)
        self.log_table.column("location", width=250)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_table.yview)
        self.log_table.configure(yscrollcommand=scrollbar.set)
        
        self.log_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load initial data
        self.refresh_log()
    
    def create_footer(self):
        """Status bar at bottom"""
        footer = ttk.Frame(self.root)
        footer.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        ttk.Label(
            footer,
            text="Press 'Q' to quit",
            foreground=Colors.TEXT_LIGHT
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            footer,
            text="Refresh Log",
            command=self.refresh_log
        ).pack(side=tk.RIGHT)
    
    def start_camera(self):
        """Initialize camera feed"""
        if not self.cap:
            self.cap = cv2.VideoCapture(0)
            self.status_label.config(text="Camera: ON", foreground=Colors.SUCCESS)
            self.show_camera_feed()
    
    def show_camera_feed(self):
        """Update camera frame in GUI"""
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                # Convert to RGB and resize
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (640, 480))
                
                # Convert to Tkinter image
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update label
                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk)
                
                # Schedule next update
                self.camera_label.after(10, self.show_camera_feed)
    
    def mark_attendance(self):
        """Capture and process attendance"""
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                
                if face_locations:
                    # ... (Add face recognition logic)
                    self.refresh_log()
                    messagebox.showinfo("Success", f"Attendance marked for {name}")
    
    def refresh_log(self):
        """Reload attendance records"""
        for item in self.log_table.get_children():
            self.log_table.delete(item)
            
        records = get_all_records()
        for record in records:
            self.log_table.insert("", "end", values=record)
    
    def on_close(self):
        """Cleanup on window close"""
        if self.cap:
            self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GeoFaceApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()