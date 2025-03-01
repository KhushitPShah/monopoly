import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                             QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, 
                             QStackedWidget, QLineEdit, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor, QIcon, QPalette

# Constants
DEFAULT_BALANCE = 1500000  # Default starting balance (1.5M)
DATA_FILE = "monopoly_cards.json"

class MonopolyTransactor(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # App state
        self.current_mode = "idle"  # idle, transfer, bidding, loan
        self.current_card = None
        self.sender_card = None
        self.receiver_card = None
        self.amount = 0
        self.base_bid = 0
        self.current_bid = 0
        
        # Load or initialize card data
        self.load_card_data()
        
        # Setup UI
        self.init_ui()
        
    def load_card_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    self.cards = json.load(f)
            else:
                # Initialize with default data for two cards
                self.cards = {
                    "card1": {
                        "balance": DEFAULT_BALANCE,
                        "transactions": 0,
                        "loans": []
                    },
                    "card2": {
                        "balance": DEFAULT_BALANCE,
                        "transactions": 0,
                        "loans": []
                    }
                }
                self.save_card_data()
        except Exception as e:
            print(f"Error loading card data: {e}")
            # Fallback to defaults
            self.cards = {
                "card1": {"balance": DEFAULT_BALANCE, "transactions": 0, "loans": []},
                "card2": {"balance": DEFAULT_BALANCE, "transactions": 0, "loans": []}
            }
    
    def save_card_data(self):
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.cards, f, indent=4)
        except Exception as e:
            print(f"Error saving card data: {e}")
            
    def init_ui(self):
        self.setWindowTitle("Monopoly Transactor")
        self.setMinimumSize(600, 800)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Status display area
        self.status_frame = QFrame()
        self.status_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.status_frame.setFrameShadow(QFrame.Shadow.Raised)
        status_layout = QVBoxLayout(self.status_frame)
        
        self.mode_label = QLabel("Mode: Idle")
        self.mode_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.balance_label = QLabel("Balance: -")
        self.balance_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.message_label = QLabel("Tap a card to begin")
        self.message_label.setFont(QFont("Arial", 14))
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        status_layout.addWidget(self.mode_label)
        status_layout.addWidget(self.balance_label)
        status_layout.addWidget(self.message_label)
        
        main_layout.addWidget(self.status_frame)
        
        # Card simulation buttons
        card_sim_layout = QHBoxLayout()
        
        self.card1_button = QPushButton("Simulate Card 1")
        self.card1_button.setFont(QFont("Arial", 12))
        self.card1_button.clicked.connect(lambda: self.simulate_card_tap("card1"))
        
        self.card2_button = QPushButton("Simulate Card 2")
        self.card2_button.setFont(QFont("Arial", 12))
        self.card2_button.clicked.connect(lambda: self.simulate_card_tap("card2"))
        
        card_sim_layout.addWidget(self.card1_button)
        card_sim_layout.addWidget(self.card2_button)
        
        main_layout.addLayout(card_sim_layout)
        
        # Mode buttons
        mode_layout = QHBoxLayout()
        
        self.transfer_button = QPushButton("Transfer")
        self.transfer_button.setFont(QFont("Arial", 12))
        self.transfer_button.clicked.connect(self.start_transfer_mode)
        
        self.bidding_button = QPushButton("Bidding")
        self.bidding_button.setFont(QFont("Arial", 12))
        self.bidding_button.clicked.connect(self.start_bidding_mode)
        
        self.loan_button = QPushButton("Loan")
        self.loan_button.setFont(QFont("Arial", 12))
        self.loan_button.clicked.connect(self.start_loan_mode)
        
        self.repay_button = QPushButton("Repay")
        self.repay_button.setFont(QFont("Arial", 12))
        self.repay_button.clicked.connect(self.start_repay_mode)
        
        mode_layout.addWidget(self.transfer_button)
        mode_layout.addWidget(self.bidding_button)
        mode_layout.addWidget(self.loan_button)
        mode_layout.addWidget(self.repay_button)
        
        main_layout.addLayout(mode_layout)
        
        # Stacked widget for different input methods
        self.stacked_widget = QStackedWidget()
        
        # Keypad widget
        keypad_widget = QWidget()
        keypad_layout = QVBoxLayout(keypad_widget)
        
        self.amount_display = QLineEdit()
        self.amount_display.setReadOnly(True)
        self.amount_display.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.amount_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        keypad_layout.addWidget(self.amount_display)
        
        # Keypad grid
        keypad_grid = QGridLayout()
        
        # Add number buttons
        for i in range(1, 10):
            row = (i-1) // 3
            col = (i-1) % 3
            button = QPushButton(str(i))
            button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            button.setMinimumSize(80, 80)
            button.clicked.connect(lambda _, digit=i: self.keypad_press(str(digit)))
            keypad_grid.addWidget(button, row, col)
        
        # Add 0, 00, 000 buttons
        zero_button = QPushButton("0")
        zero_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        zero_button.setMinimumSize(80, 80)
        zero_button.clicked.connect(lambda: self.keypad_press("0"))
        keypad_grid.addWidget(zero_button, 3, 0)
        
        double_zero_button = QPushButton("00")
        double_zero_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        double_zero_button.setMinimumSize(80, 80)
        double_zero_button.clicked.connect(lambda: self.keypad_press("00"))
        keypad_grid.addWidget(double_zero_button, 3, 1)
        
        triple_zero_button = QPushButton("000")
        triple_zero_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        triple_zero_button.setMinimumSize(80, 80)
        triple_zero_button.clicked.connect(lambda: self.keypad_press("000"))
        keypad_grid.addWidget(triple_zero_button, 3, 2)
        
        # Control buttons
        clear_button = QPushButton("C")
        clear_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        clear_button.setMinimumSize(80, 80)
        clear_button.clicked.connect(self.clear_amount)
        keypad_grid.addWidget(clear_button, 0, 3)
        
        backspace_button = QPushButton("⌫")
        backspace_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        backspace_button.setMinimumSize(80, 80)
        backspace_button.clicked.connect(self.backspace_amount)
        keypad_grid.addWidget(backspace_button, 1, 3)
        
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.confirm_button.setMinimumSize(80, 170)
        self.confirm_button.clicked.connect(self.confirm_amount)
        keypad_grid.addWidget(self.confirm_button, 2, 3, 2, 1)
        
        keypad_layout.addLayout(keypad_grid)
        
        # Bidding widget
        bidding_widget = QWidget()
        bidding_layout = QVBoxLayout(bidding_widget)
        
        bid_display_layout = QHBoxLayout()
        self.bid_display = QLabel("Current Bid: 0")
        self.bid_display.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.bid_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bid_display_layout.addWidget(self.bid_display)
        
        bidding_layout.addLayout(bid_display_layout)
        
        # Bid increment buttons
        bid_increment_layout = QGridLayout()
        
        increment_values = [100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
        
        for i, value in enumerate(increment_values):
            display_value = self.format_amount_short(value)
            row = i // 3
            col = i % 3
            button = QPushButton(f"+{display_value}")
            button.setFont(QFont("Arial", 14))
            button.setMinimumSize(80, 60)
            button.clicked.connect(lambda _, v=value: self.add_to_bid(v))
            bid_increment_layout.addWidget(button, row, col)
        
        bidding_layout.addLayout(bid_increment_layout)
        
        # Bid control buttons
        bid_control_layout = QHBoxLayout()
        
        bid_clear_button = QPushButton("Clear")
        bid_clear_button.setFont(QFont("Arial", 14))
        bid_clear_button.clicked.connect(self.clear_bid)
        
        bid_confirm_button = QPushButton("Confirm Bid")
        bid_confirm_button.setFont(QFont("Arial", 14))
        bid_confirm_button.clicked.connect(self.confirm_bid)
        
        bid_control_layout.addWidget(bid_clear_button)
        bid_control_layout.addWidget(bid_confirm_button)
        
        bidding_layout.addLayout(bid_control_layout)
        
        # Add widgets to stacked widget
        self.stacked_widget.addWidget(keypad_widget)  # Index 0: Keypad
        self.stacked_widget.addWidget(bidding_widget)  # Index 1: Bidding
        
        main_layout.addWidget(self.stacked_widget)
        
        # Reset button
        reset_layout = QHBoxLayout()
        
        self.reset_button = QPushButton("Reset Mode")
        self.reset_button.setFont(QFont("Arial", 12))
        self.reset_button.clicked.connect(self.reset_to_idle)
        
        reset_layout.addStretch()
        reset_layout.addWidget(self.reset_button)
        
        main_layout.addLayout(reset_layout)
        
        # Set the central widget
        self.setCentralWidget(main_widget)
        
        # Initially hide the stacked widget
        self.stacked_widget.setVisible(False)
    
    def simulate_card_tap(self, card_id):
        self.current_card = card_id
        
        # Handle the card tap based on the current mode
        if self.current_mode == "idle":
            self.display_balance(card_id)
        elif self.current_mode == "transfer_sender":
            self.sender_card = card_id
            self.display_balance(card_id)
            self.message_label.setText("Enter amount to transfer")
            self.current_mode = "transfer_amount"
            self.stacked_widget.setCurrentIndex(0)  # Show keypad
            self.stacked_widget.setVisible(True)
            self.clear_amount()
        elif self.current_mode == "transfer_receiver":
            self.receiver_card = card_id
            self.process_transfer()
        elif self.current_mode == "bidding_card":
            self.display_balance(card_id)
            self.message_label.setText("Enter base bid amount")
            self.current_mode = "bidding_base"
            self.stacked_widget.setCurrentIndex(0)  # Show keypad
            self.stacked_widget.setVisible(True)
            self.clear_amount()
        elif self.current_mode == "bidding_final":
            self.process_bid(card_id)
        elif self.current_mode == "loan_card":
            self.display_balance(card_id)
            self.message_label.setText("Enter loan amount")
            self.current_mode = "loan_amount"
            self.stacked_widget.setCurrentIndex(0)  # Show keypad
            self.stacked_widget.setVisible(True)
            self.clear_amount()
        elif self.current_mode == "repay_card":
            self.process_repayment(card_id)
    
    def display_balance(self, card_id):
        card_data = self.cards[card_id]
        balance = card_data["balance"]
        transactions = card_data["transactions"]
        
        formatted_balance = self.format_amount(balance)
        self.balance_label.setText(f"Balance: {formatted_balance}")
        
        if transactions > 0:
            self.message_label.setText(f"Please repay {transactions}")
        else:
            self.message_label.setText(f"Card {card_id[-1]} - Ready")
    
    def format_amount(self, amount):
        if amount >= 1000000:
            return f"{amount/1000000:.2f}M".rstrip('0').rstrip('.') + "M"
        elif amount >= 1000:
            return f"{amount/1000:.2f}K".rstrip('0').rstrip('.') + "K"
        else:
            return str(amount)
    
    def format_amount_short(self, amount):
        if amount >= 1000000:
            return f"{int(amount/1000000)}M"
        elif amount >= 1000:
            return f"{int(amount/1000)}K"
        else:
            return str(amount)
    
    def keypad_press(self, digit):
        current_text = self.amount_display.text().replace(",", "")
        
        # Prevent adding too many digits
        if len(current_text) > 8:
            return
            
        new_amount = current_text + digit
        formatted_amount = self.format_display_amount(new_amount)
        self.amount_display.setText(formatted_amount)
    
    def format_display_amount(self, amount_str):
        # Remove any non-digit characters
        clean_amount = ''.join(c for c in amount_str if c.isdigit())
        
        # Convert to integer
        if clean_amount:
            amount = int(clean_amount)
            # Use locale to format with commas
            return f"{amount:,}"
        return ""
    
    def clear_amount(self):
        self.amount_display.setText("")
    
    def backspace_amount(self):
        current_text = self.amount_display.text().replace(",", "")
        if current_text:
            new_text = current_text[:-1]
            formatted_amount = self.format_display_amount(new_text)
            self.amount_display.setText(formatted_amount)
    
    def confirm_amount(self):
        try:
            amount_text = self.amount_display.text().replace(",", "")
            
            if not amount_text:
                self.message_label.setText("Please enter an amount")
                return
                
            amount = int(amount_text)
            
            if amount <= 0:
                self.message_label.setText("Amount must be greater than 0")
                return
            
            if self.current_mode == "transfer_amount":
                # Check if sender has enough funds
                if amount > self.cards[self.sender_card]["balance"]:
                    self.message_label.setText("Insufficient funds")
                    return
                    
                self.amount = amount
                self.message_label.setText("Tap receiver's card")
                self.current_mode = "transfer_receiver"
                self.stacked_widget.setVisible(False)
                
            elif self.current_mode == "bidding_base":
                self.base_bid = amount
                self.current_bid = amount
                self.bid_display.setText(f"Current Bid: {self.format_amount(amount)}")
                self.message_label.setText("Adjust bid with increments")
                self.current_mode = "bidding_increment"
                self.stacked_widget.setCurrentIndex(1)  # Show bidding widget
                
            elif self.current_mode == "loan_amount":
                self.amount = amount
                self.process_loan()
                
        except ValueError:
            self.message_label.setText("Invalid amount")
    
    def start_transfer_mode(self):
        self.reset_to_idle()
        self.current_mode = "transfer_sender"
        self.mode_label.setText("Mode: Transfer")
        self.message_label.setText("Tap sender's card")
    
    def start_bidding_mode(self):
        self.reset_to_idle()
        self.current_mode = "bidding_card"
        self.mode_label.setText("Mode: Bidding")
        self.message_label.setText("Tap card of bidder")
    
    def start_loan_mode(self):
        self.reset_to_idle()
        self.current_mode = "loan_card"
        self.mode_label.setText("Mode: Loan")
        self.message_label.setText("Tap card to receive loan")
    
    def start_repay_mode(self):
        self.reset_to_idle()
        self.current_mode = "repay_card"
        self.mode_label.setText("Mode: Repay")
        self.message_label.setText("Tap card to repay loan")
    
    def process_transfer(self):
        if self.sender_card == self.receiver_card:
            self.message_label.setText("Cannot transfer to the same card")
            return
            
        try:
            # Deduct from sender
            self.cards[self.sender_card]["balance"] -= self.amount
            
            # Add to receiver
            self.cards[self.receiver_card]["balance"] += self.amount
            
            # Display the new balance of the receiver
            self.display_balance(self.receiver_card)
            
            # Update message
            sender_card_num = self.sender_card[-1]
            receiver_card_num = self.receiver_card[-1]
            amount_str = self.format_amount(self.amount)
            self.message_label.setText(f"Transferred {amount_str} from Card {sender_card_num} to Card {receiver_card_num}")
            
            # Save changes
            self.save_card_data()
            
            # Reset after a short delay
            QTimer.singleShot(3000, self.reset_to_idle)
            
        except Exception as e:
            self.message_label.setText(f"Error: {str(e)}")
    
    def add_to_bid(self, increment):
        self.current_bid += increment
        self.bid_display.setText(f"Current Bid: {self.format_amount(self.current_bid)}")
    
    def clear_bid(self):
        self.current_bid = self.base_bid
        self.bid_display.setText(f"Current Bid: {self.format_amount(self.base_bid)}")
    
    def confirm_bid(self):
        if self.current_bid <= 0:
            self.message_label.setText("Bid must be greater than 0")
            return
            
        self.message_label.setText("Tap card to confirm and pay bid")
        self.current_mode = "bidding_final"
        self.stacked_widget.setVisible(False)
    
    def process_bid(self, card_id):
        try:
            # Check if card has enough funds
            if self.current_bid > self.cards[card_id]["balance"]:
                self.message_label.setText("Insufficient funds for bid")
                return
                
            # Deduct bid amount from card
            self.cards[card_id]["balance"] -= self.current_bid
            
            # Increment transactions counter
            self.cards[card_id]["transactions"] += 1
            
            # Display the new balance
            self.display_balance(card_id)
            
            # Update message
            amount_str = self.format_amount(self.current_bid)
            self.message_label.setText(f"Bid of {amount_str} paid successfully")
            
            # Save changes
            self.save_card_data()
            
            # Reset after a short delay
            QTimer.singleShot(3000, self.reset_to_idle)
            
        except Exception as e:
            self.message_label.setText(f"Error: {str(e)}")
    
    def process_loan(self):
        try:
            # Add loan amount to card
            self.cards[self.current_card]["balance"] += self.amount
            
            # Store loan information
            self.cards[self.current_card]["loans"].append({
                "amount": self.amount,
                "paid": False
            })
            
            # Display the new balance
            self.display_balance(self.current_card)
            
            # Update message
            amount_str = self.format_amount(self.amount)
            self.message_label.setText(f"Loan of {amount_str} added successfully")
            
            # Save changes
            self.save_card_data()
            
            # Reset after a short delay
            QTimer.singleShot(3000, self.reset_to_idle)
            
        except Exception as e:
            self.message_label.setText(f"Error: {str(e)}")
    
    def process_repayment(self, card_id):
        try:
            card_data = self.cards[card_id]
            transactions = card_data["transactions"]
            
            if transactions == 0:
                self.message_label.setText("No loans to repay")
                return
                
            # Calculate interest (5% base + 1% per transaction after the first)
            interest_rate = 0.05
            if transactions > 1:
                interest_rate += (transactions - 1) * 0.01
                
            # Find unpaid loans
            unpaid_loans = [loan for loan in card_data["loans"] if not loan["paid"]]
            
            if not unpaid_loans:
                self.message_label.setText("No unpaid loans found")
                return
                
            # Calculate total repayment amount
            loan_total = sum(loan["amount"] for loan in unpaid_loans)
            interest_amount = loan_total * interest_rate
            total_repayment = loan_total + int(interest_amount)
            
            # Check if card has enough balance
            if total_repayment > card_data["balance"]:
                self.message_label.setText("Insufficient funds to repay loans")
                return
                
            # Deduct repayment amount
            card_data["balance"] -= total_repayment
            
            # Mark loans as paid
            for loan in unpaid_loans:
                loan["paid"] = True
                
            # Reset transaction counter
            card_data["transactions"] = 0
            
            # Display the new balance
            self.display_balance(card_id)
            
            # Update message
            repayment_str = self.format_amount(total_repayment)
            interest_str = self.format_amount(int(interest_amount))
            self.message_label.setText(f"Repaid {repayment_str} (incl. {interest_str} interest)")
            
            # Save changes
            self.save_card_data()
            
            # Reset after a short delay
            QTimer.singleShot(3000, self.reset_to_idle)
            
        except Exception as e:
            self.message_label.setText(f"Error: {str(e)}")
    
    def reset_to_idle(self):
        self.current_mode = "idle"
        self.mode_label.setText("Mode: Idle")
        self.message_label.setText("Tap a card to begin")
        self.balance_label.setText("Balance: -")
        self.stacked_widget.setVisible(False)
        self.sender_card = None
        self.receiver_card = None
        self.amount = 0
        self.base_bid = 0
        self.current_bid = 0
        self.current_card = None

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show the main window
    window = MonopolyTransactor()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
