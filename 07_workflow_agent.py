"""
Exercise 7: Workflow Agent - Multi-step Business Workflows
==========================================================

Learning Objectives:
- Understand how to build multi-step workflows
- Learn about workflow orchestration and state management
- See human-in-the-loop patterns in action

This agent demonstrates workflow automation - breaking complex tasks
into steps and executing them systematically.
"""

import os
from enum import Enum
from typing import Dict, Any
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.toolkit import Toolkit

load_dotenv()

class WorkflowState(Enum):
    """Workflow execution states"""
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    SENT = "sent"
    COMPLETED = "completed"

class EmailWorkflowToolkit(Toolkit):
    """Toolkit for email workflow automation"""

    def __init__(self):
        super().__init__(name="email_workflow")
        self.workflow_state = WorkflowState.DRAFT
        self.email_draft = {}
        self.register(self.draft_email)
        self.register(self.review_email)
        self.register(self.approve_email)
        self.register(self.send_email)
        self.register(self.get_workflow_status)

    def draft_email(self, recipient: str, subject: str, purpose: str) -> str:
        """
        Create an email draft based on purpose and recipient.

        Args:
            recipient (str): Email recipient (customer, colleague, vendor)
            subject (str): Email subject line
            purpose (str): Purpose of the email (follow-up, proposal, support, etc.)

        Returns:
            str: Created email draft
        """
        # Simulate email composition based on purpose
        templates = {
            "follow-up": f"""Dear {recipient},

I hope this email finds you well. I wanted to follow up on our recent conversation regarding {subject}.

Please let me know if you have any questions or if there's anything I can help clarify.

Best regards,
ACME Corporation""",

            "proposal": f"""Dear {recipient},

Thank you for your interest in ACME Corporation's services. I'm pleased to present our proposal for {subject}.

We believe our solution can provide significant value to your organization. I'd be happy to schedule a call to discuss the details.

Best regards,
ACME Corporation""",

            "support": f"""Dear {recipient},

Thank you for contacting ACME Corporation support regarding {subject}.

We've reviewed your request and are working on a solution. I'll keep you updated on our progress.

If you have any urgent concerns, please don't hesitate to reach out.

Best regards,
ACME Support Team"""
        }

        # Generate appropriate email based on purpose
        if purpose.lower() in templates:
            email_body = templates[purpose.lower()]
        else:
            email_body = f"""Dear {recipient},

Thank you for your message regarding {subject}.

I'll get back to you with more information shortly.

Best regards,
ACME Corporation"""

        self.email_draft = {
            "recipient": recipient,
            "subject": subject,
            "body": email_body,
            "purpose": purpose
        }
        self.workflow_state = WorkflowState.DRAFT

        return f"📝 Email draft created:\n\nTo: {recipient}\nSubject: {subject}\n\n{email_body}\n\n✅ Status: {self.workflow_state.value}"

    def review_email(self, feedback: str = None) -> str:
        """
        Review the email draft and provide feedback.

        Args:
            feedback (str): Optional feedback for improvements

        Returns:
            str: Review results and recommendations
        """
        if not self.email_draft:
            return "❌ No email draft to review. Please create a draft first."

        self.workflow_state = WorkflowState.REVIEW

        # Simulate review process
        review_points = []

        # Check subject line
        subject = self.email_draft["subject"]
        if len(subject) < 5:
            review_points.append("📧 Subject line seems too short")
        elif len(subject) > 50:
            review_points.append("📧 Subject line might be too long")

        # Check body content
        body = self.email_draft["body"]
        if len(body) < 50:
            review_points.append("📝 Email body seems very brief")
        elif "ACME Corporation" not in body:
            review_points.append("🏢 Consider adding company branding")

        # Add custom feedback
        if feedback:
            review_points.append(f"💭 Human feedback: {feedback}")

        if not review_points:
            review_points.append("✅ Email looks good, ready for approval")

        review_summary = "\n".join(f"• {point}" for point in review_points)

        return f"🔍 Email Review Complete:\n\n{review_summary}\n\n✅ Status: {self.workflow_state.value}"

    def approve_email(self, approved: bool = True) -> str:
        """
        Approve or reject the email for sending.

        Args:
            approved (bool): Whether to approve the email

        Returns:
            str: Approval status
        """
        if not self.email_draft:
            return "❌ No email draft to approve."

        if self.workflow_state != WorkflowState.REVIEW:
            return "❌ Email must be reviewed before approval."

        if approved:
            self.workflow_state = WorkflowState.APPROVED
            return f"✅ Email approved for sending!\n\n📧 Ready to send to: {self.email_draft['recipient']}\n✅ Status: {self.workflow_state.value}"
        else:
            self.workflow_state = WorkflowState.DRAFT
            return f"❌ Email rejected. Please revise the draft.\n✅ Status: {self.workflow_state.value}"

    def send_email(self) -> str:
        """
        Send the approved email.

        Returns:
            str: Send confirmation
        """
        if not self.email_draft:
            return "❌ No email draft to send."

        if self.workflow_state != WorkflowState.APPROVED:
            return "❌ Email must be approved before sending."

        # Simulate sending
        self.workflow_state = WorkflowState.SENT

        return f"""📧 Email sent successfully!

To: {self.email_draft['recipient']}
Subject: {self.email_draft['subject']}
Time: Just now

✅ Status: {self.workflow_state.value}

🎉 Workflow completed successfully!"""

    def get_workflow_status(self) -> str:
        """
        Get current workflow status and next steps.

        Returns:
            str: Current status and available actions
        """
        if not self.email_draft:
            return "📋 Workflow Status: No active workflow\n\n🚀 Next: Create an email draft"

        next_steps = {
            WorkflowState.DRAFT: "🔍 Next: Review the email",
            WorkflowState.REVIEW: "✅ Next: Approve or reject the email",
            WorkflowState.APPROVED: "📧 Next: Send the email",
            WorkflowState.SENT: "🎉 Workflow completed!",
        }

        status_info = f"""📋 Current Workflow Status: {self.workflow_state.value.upper()}

📧 Email Details:
• To: {self.email_draft['recipient']}
• Subject: {self.email_draft['subject']}
• Purpose: {self.email_draft['purpose']}

{next_steps.get(self.workflow_state, "Unknown next step")}"""

        return status_info

def main():
    print("📋 Exercise 7: Workflow Agent")
    print("=" * 40)
    print("This agent manages multi-step email workflows!")
    print("Draft → Review → Approve → Send")
    print("Type 'exit' to quit.\n")

    # Create workflow agent
    agent = Agent(
        model=Groq(
            id="llama-3.3-70b-versatile",
            max_tokens=1000
        ),
        description="""You are a workflow automation assistant that helps manage
        email workflows. You can draft emails, review them, get approval, and send them.

        Always follow the proper workflow order:
        1. Draft email (draft_email)
        2. Review email (review_email)
        3. Approve email (approve_email)
        4. Send email (send_email)

        Use get_workflow_status to check current progress.""",

        tools=[EmailWorkflowToolkit()],
        markdown=True
    )

    print("💡 Workflow commands:")
    print("  📝 'Draft an email to [recipient] about [subject]'")
    print("  🔍 'Review the email'")
    print("  ✅ 'Approve the email' or 'Reject the email'")
    print("  📧 'Send the email'")
    print("  📋 'What's the workflow status?'")
    print()

    print("🎮 Try this workflow:")
    print("1. 'Draft a follow-up email to john@customer.com about our recent meeting'")
    print("2. 'Review the email'")
    print("3. 'Approve the email'")
    print("4. 'Send the email'")
    print()

    while True:
        try:
            user_input = input("Workflow Command: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Goodbye! 👋")
                break

            print("\nWorkflow Agent:")
            agent.print_response(user_input, stream=False)
            print()

        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in environment variables.")
        exit(1)

    main()

"""
🎯 Try these workflow scenarios:

Complete Workflow:
1. "Draft a proposal email to sarah@startup.com about our AI consulting services"
2. "Review the email draft"
3. "The email looks good, please approve it"
4. "Send the approved email"
5. "What's the current workflow status?"

Workflow with Feedback:
1. "Create a support email to mike@company.com about his login issue"
2. "Review the email and suggest it needs more technical details"
3. "Reject the email for revision"
4. "Check workflow status"

Testing Workflow Rules:
1. "Send an email" (should fail - no draft)
2. "Approve an email" (should fail - no review)
3. "Draft an email to test@example.com about testing"
4. "Send the email" (should fail - not approved)

🧠 Key Concepts:
- Workflow state management with enums
- Sequential step enforcement
- Human-in-the-loop approval process
- State validation before actions
- Business process automation

🔧 Workflow Patterns:
- State machines for process control
- Validation gates between steps
- Rollback capabilities (reject → draft)
- Status tracking and reporting
- Template-based content generation

🎨 Real-World Applications:
- Approval workflows
- Content publishing pipelines
- Customer onboarding processes
- Document review cycles
- Order processing workflows

📝 Next: In 08_specialized_agents.py, we'll coordinate multiple specialized agents!
"""