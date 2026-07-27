import os
import csv
import random

DATASET_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(DATASET_DIR, "resumes_dataset.csv")

CATEGORIES_CONFIG = {
    "Data Scientist": {
        "skills": ["Python", "R", "SQL", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-Learn", "Pandas", "NumPy", "Statistics", "Data Mining"],
        "titles": ["Senior Data Scientist", "Data Scientist", "Lead AI Researcher", "Quantitative Analyst"],
        "education": ["MS in Data Science", "PhD in Computer Science", "BS in Statistics", "MS in Applied Mathematics"],
        "companies": ["TechAnalytics Inc.", "DataCorp Global", "AI Ventures", "Insight Labs"],
        "responsibilities": [
            "Developed predictive models using XGBoost and Random Forest resulting in 18% accuracy improvement.",
            "Engineered ETL data pipelines in PySpark and SQL processing over 50GB of daily log data.",
            "Designed and deployed A/B testing frameworks to optimize customer retention metrics.",
            "Utilized NLTK and SpaCy for sentiment analysis on customer feedback datasets."
        ]
    },
    "Frontend Developer": {
        "skills": ["JavaScript", "TypeScript", "React", "Vue.js", "Angular", "HTML5", "CSS3", "Sass", "Tailwind CSS", "Next.js", "Redux", "Webpack", "Figma"],
        "titles": ["Frontend Developer", "Senior UI Engineer", "React Developer", "Web Developer"],
        "education": ["BS in Computer Science", "BS in Web Development", "Coding Bootcamp Certificate"],
        "companies": ["WebCraft Studio", "PixelPerfect Media", "Frontier Digital", "AppFlow Systems"],
        "responsibilities": [
            "Built responsive Single Page Applications (SPAs) using React.js and Redux Toolkit.",
            "Integrated RESTful APIs and GraphQL endpoints for real-time web interface updates.",
            "Optimized web application bundle sizes and lighthouse performance scores by 35%.",
            "Collaborated with UI/UX designers in Figma to build accessible, cross-browser UI components."
        ]
    },
    "Backend Developer": {
        "skills": ["Python", "Java", "Node.js", "Go", "C#", "Django", "Flask", "Spring Boot", "Express", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Docker", "REST API"],
        "titles": ["Backend Engineer", "Senior Software Engineer", "API Developer", "Java Developer"],
        "education": ["BS in Computer Science", "MS in Software Engineering", "BS in Information Technology"],
        "companies": ["CoreStack Systems", "ServerLess Tech", "MicroService Corp", "CloudNexus"],
        "responsibilities": [
            "Designed microservices architecture using Node.js and Express handling 1M daily requests.",
            "Implemented JWT authentication and OAuth2 SSO authorization standards.",
            "Optimized PostgreSQL database query execution plans, reducing latency by 40%.",
            "Configured Redis caching layer for quick lookup of high-demand user session records."
        ]
    },
    "Full Stack Developer": {
        "skills": ["JavaScript", "TypeScript", "Python", "React", "Node.js", "Express", "MongoDB", "PostgreSQL", "HTML", "CSS", "AWS", "Git", "Docker", "REST API"],
        "titles": ["Full Stack Engineer", "Senior Software Developer", "Full Stack Architect"],
        "education": ["BS in Computer Science", "MS in Information Systems", "Bootcamp Graduate"],
        "companies": ["OmniTech Solutions", "StackOverflow Inc.", "BuildFast Labs", "Synergy Software"],
        "responsibilities": [
            "Developed end-to-end SaaS applications leveraging React for frontend and Node.js for backend.",
            "Maintained MongoDB and PostgreSQL database schemas and migrations.",
            "Automated CI/CD deployment pipelines using GitHub Actions and AWS EC2 instances.",
            "Created RESTful endpoints and interactive web UI for client management portal."
        ]
    },
    "DevOps Engineer": {
        "skills": ["Docker", "Kubernetes", "Terraform", "Ansible", "AWS", "Azure", "GCP", "Jenkins", "GitLab CI", "Linux", "Bash", "Python", "Prometheus", "Grafana"],
        "titles": ["DevOps Engineer", "Site Reliability Engineer (SRE)", "Infrastructure Engineer"],
        "education": ["BS in Computer Science", "BS in Network Engineering", "AWS Certified DevOps Engineer"],
        "companies": ["CloudCloud Infra", "ReliableOps Systems", "Skyline Cloud", "ScaleTech"],
        "responsibilities": [
            "Managed Kubernetes clusters in AWS EKS across staging and production environments.",
            "Wrote Infrastructure as Code (IaC) templates in Terraform for automated AWS cloud provision.",
            "Built CI/CD automated deployment pipelines with GitLab CI and Docker containerization.",
            "Set up monitoring and alerting dashboards using Prometheus and Grafana."
        ]
    },
    "Machine Learning Engineer": {
        "skills": ["Python", "TensorFlow", "PyTorch", "Keras", "Scikit-Learn", "OpenCV", "NLP", "LLMs", "Transformers", "CUDA", "Docker", "MLflow", "Kubeflow"],
        "titles": ["Machine Learning Engineer", "AI Engineer", "Deep Learning Research Specialist"],
        "education": ["MS in Artificial Intelligence", "PhD in Computer Vision", "BS in Computer Science"],
        "companies": ["NeuralNetworks AI", "DeepMinded Tech", "VisionML Solutions", "Cognitive AI"],
        "responsibilities": [
            "Trained computer vision models for object detection using YOLOv8 and PyTorch.",
            "Fine-tuned Large Language Models (LLMs) with LoRA and HuggingFace Transformers.",
            "Containerized ML models using Docker and deployed REST inference endpoints on AWS SageMaker.",
            "Implemented MLflow tracking for experiment logging and model artifact versioning."
        ]
    },
    "Cloud Architect": {
        "skills": ["AWS", "Azure", "GCP", "Cloud Architecture", "Serverless", "Lambda", "Terraform", "Security", "Networking", "IAM", "VPC", "Kubernetes", "Cost Optimization"],
        "titles": ["Cloud Architect", "Senior Solutions Architect", "Enterprise Cloud Consultant"],
        "education": ["BS in Computer Science", "AWS Certified Solutions Architect Professional", "Azure Solutions Architect"],
        "companies": ["Enterprise Cloud Inc.", "Horizon Solutions", "Global Cloud Consulting", "Vertex Cloud"],
        "responsibilities": [
            "Designed multi-region fault-tolerant AWS infrastructure architectures for financial systems.",
            "Migrated legacy on-premise monolithic applications to AWS cloud serverless microservices.",
            "Implemented cloud governance, IAM security policies, and VPC peering connections.",
            "Reduced client enterprise cloud infrastructure spending by $120,000 annually."
        ]
    },
    "Cybersecurity Specialist": {
        "skills": ["Cybersecurity", "Penetration Testing", "Ethical Hacking", "Network Security", "Wireshark", "Metasploit", "SIEM", "Splunk", "Firewalls", "CISSP", "CEH", "Cryptography"],
        "titles": ["Cybersecurity Specialist", "Information Security Officer", "Penetration Tester", "SOC Analyst"],
        "education": ["BS in Cybersecurity", "MS in Information Security", "CISSP Certified"],
        "companies": ["SecureGuard Defense", "CyberShield Inc.", "ThreatHunter Cyber", "Fortress Security"],
        "responsibilities": [
            "Conducted penetration testing and vulnerability assessments on enterprise web applications.",
            "Monitored network security logs using Splunk SIEM to detect and neutralize threat intrusions.",
            "Implemented multi-factor authentication (MFA) and zero-trust network access controls.",
            "Drafted incident response protocols and conducted security awareness training for staff."
        ]
    },
    "Mobile App Developer": {
        "skills": ["Swift", "Kotlin", "React Native", "Flutter", "iOS", "Android", "Mobile UI", "Xcode", "Android Studio", "SQLite", "Firebase", "REST API", "Git"],
        "titles": ["Mobile App Developer", "iOS Developer", "Android Engineer", "React Native Developer"],
        "education": ["BS in Computer Science", "BS in Mobile Computing", "Software Engineering Diploma"],
        "companies": ["AppStudio Mobile", "PocketSoft", "TouchInterface", "Mobility Labs"],
        "responsibilities": [
            "Developed cross-platform mobile apps for iOS and Android using React Native and Flutter.",
            "Published apps to Apple App Store and Google Play Store with 100,000+ total downloads.",
            "Implemented push notification integration via Firebase Cloud Messaging (FCM).",
            "Integrated offline data synchronization using SQLite and Async Storage."
        ]
    },
    "Database Administrator": {
        "skills": ["PostgreSQL", "MySQL", "Oracle", "SQL Server", "MongoDB", "Database Tuning", "Backup & Recovery", "Replication", "ETL", "PL/SQL", "T-SQL", "Performance Tuning"],
        "titles": ["Database Administrator (DBA)", "Senior SQL Developer", "Data Platform Engineer"],
        "education": ["BS in Information Systems", "Oracle Certified Professional", "BS in Computer Science"],
        "companies": ["DataStore Inc.", "DB Reliant", "InfoBase Systems", "Enterprise Storage"],
        "responsibilities": [
            "Managed and maintained high-availability Oracle and PostgreSQL database clusters.",
            "Automated database backup, recovery, and point-in-time restore procedures.",
            "Optimized complex SQL queries, indexes, and execution plans for database performance.",
            "Configured master-slave database replication and disaster recovery failover nodes."
        ]
    },
    "UI/UX Designer": {
        "skills": ["Figma", "Adobe XD", "Photoshop", "Illustrator", "Wireframing", "Prototyping", "User Research", "Usability Testing", "Design Systems", "UI Design", "UX Design"],
        "titles": ["UI/UX Designer", "Product Designer", "User Experience Researcher", "Lead Visual Designer"],
        "education": ["BA in Interaction Design", "BS in Graphic Design", "HCI Certificate"],
        "companies": ["CreativeFlow Agency", "UserFirst Designs", "Studio Minimal", "Interactive Experience"],
        "responsibilities": [
            "Created high-fidelity interactive wireframes and prototypes in Figma and Adobe XD.",
            "Conducted user research interviews and usability testing sessions with 50+ participants.",
            "Established comprehensive multi-brand Design Systems and visual style guides.",
            "Collaborated closely with frontend developers to ensure 100% pixel-perfect UI delivery."
        ]
    },
    "Software QA Engineer": {
        "skills": ["Selenium", "Cypress", "Postman", "JUnit", "PyTest", "Test Automation", "Manual Testing", "Jira", "Jenkins", "API Testing", "LoadRunner", "Regression Testing"],
        "titles": ["Software QA Engineer", "QA Automation Lead", "Software Test Engineer"],
        "education": ["BS in Computer Science", "ISTQB Certified Tester", "BS in Information Technology"],
        "companies": ["QualityFirst Tech", "TestPro Solutions", "BugFree Systems", "AssureSoft"],
        "responsibilities": [
            "Built automated E2E test suites using Selenium WebDriver and Python PyTest.",
            "Executed automated REST API testing in Postman and Newman command-line scripts.",
            "Tracked and managed software bug reports in Jira with clear steps for engineering teams.",
            "Integrated automated test runs into CI/CD build pipelines using Jenkins."
        ]
    },
    "Data Analyst": {
        "skills": ["SQL", "Excel", "Power BI", "Tableau", "Python", "Pandas", "Data Visualization", "Google Analytics", "Statistics", "Reporting", "A/B Testing"],
        "titles": ["Data Analyst", "Business Intelligence Analyst", "Senior Reporting Specialist"],
        "education": ["BS in Economics", "BS in Data Analytics", "BS in Business Information Systems"],
        "companies": ["Insightful Analytics", "MetricWorks", "BusinessData Corp", "Visionary Metrics"],
        "responsibilities": [
            "Constructed interactive executive dashboards in Power BI and Tableau connected to SQL databases.",
            "Extracted and cleaned large datasets using SQL queries and Python Pandas scripts.",
            "Presented monthly business metrics and data-driven growth recommendations to stakeholders.",
            "Analyzed customer cohort retention and funnel conversion rates."
        ]
    },
    "System Administrator": {
        "skills": ["Linux", "Ubuntu", "CentOS", "Windows Server", "Active Directory", "DNS", "DHCP", "VMware", "Bash", "PowerShell", "Networking", "Firewalls"],
        "titles": ["System Administrator", "IT Infrastructure Administrator", "Senior Linux SysAdmin"],
        "education": ["BS in Network Administration", "CompTIA Network+", "Microsoft Certified Systems Engineer"],
        "companies": ["InfraTech Global", "SysAdmin Corp", "NetworkShield", "ServerCenter"],
        "responsibilities": [
            "Administered 150+ Linux (Ubuntu/RHEL) and Windows Server instances.",
            "Managed Active Directory, GPO policies, DNS, and DHCP enterprise domain configurations.",
            "Automated system maintenance and user account provisioning scripts in Bash and PowerShell.",
            "Configured VMware vSphere virtualization clusters and SAN storage arrays."
        ]
    },
    "IT Project Manager": {
        "skills": ["Project Management", "Agile", "Scrum", "Jira", "Confluence", "PMP", "Risk Management", "Budgeting", "Stakeholder Management", "Resource Allocation", "MS Project"],
        "titles": ["IT Project Manager", "Senior Technical Program Manager", "Agile Project Delivery Lead"],
        "education": ["BS in Business Administration", "MS in Technology Management", "PMP Certified"],
        "companies": ["DeliveryTech", "AgilePro Solutions", "PM Pinnacle", "TechExec Consulting"],
        "responsibilities": [
            "Managed end-to-end delivery of complex software products with budgets up to $2M.",
            "Facilitated daily Scrum standups, sprint planning, and retrospective sessions in Jira.",
            "Mitigated project risks and managed cross-functional engineering team communication.",
            "Delivered 95% of software initiatives on schedule and within assigned budget limits."
        ]
    },
    "Product Manager": {
        "skills": ["Product Strategy", "Product Roadmap", "User Stories", "Agile", "Jira", "Market Research", "Product Analytics", "Mixpanel", "UX", "Stakeholder Management"],
        "titles": ["Product Manager", "Senior Technical Product Manager", "Group Product Manager"],
        "education": ["BS in Computer Science", "MBA from Business School", "Certified Product Manager"],
        "companies": ["InnovateTech", "ProductVibe", "NextGen Solutions", "Apex Products"],
        "responsibilities": [
            "Defined product vision, core feature backlog, and multi-quarter strategic product roadmaps.",
            "Authored detailed user stories, acceptance criteria, and technical product requirements.",
            "Analyzed product usage metrics in Mixpanel to prioritize high-impact feature enhancements.",
            "Led cross-functional teams of engineers, UX designers, and marketers."
        ]
    },
    "Scrum Master": {
        "skills": ["Scrum", "Agile", "Kanban", "Jira", "Confluence", "Servant Leadership", "Facilitation", "Sprint Planning", "Retrospectives", "CSM", "SAFe"],
        "titles": ["Scrum Master", "Agile Coach", "Senior Scrum Master"],
        "education": ["BS in Communications", "Certified ScrumMaster (CSM)", "SAFe Agilist"],
        "companies": ["AgileWay Inc.", "SprintMasters", "Transformation Labs", "Velocity Tech"],
        "responsibilities": [
            "Guided 3 software development teams through Agile Scrum frameworks and Kanban principles.",
            "Removed technical sprint blockers and coached teams to increase sprint velocity by 25%.",
            "Facilitated transparent sprint reviews, release planning, and continuous improvement retrospectives.",
            "Maintained Jira sprint boards, burn-down charts, and team performance metrics."
        ]
    },
    "Technical Writer": {
        "skills": ["Technical Writing", "API Documentation", "Markdown", "GitBook", "Confluence", "DITA", "Swagger", "Postman", "Editing", "User Guides", "Software Manuals"],
        "titles": ["Technical Writer", "API Documentation Specialist", "Senior Content Developer"],
        "education": ["BA in English / Journalism", "BS in Technical Communication"],
        "companies": ["DocuTech Labs", "WriteWell Solutions", "ApiDocs Inc.", "DevWriter"],
        "responsibilities": [
            "Authored developer documentation, REST API references, and SDK user guides using Markdown.",
            "Created interactive API code examples and OpenAPI / Swagger specifications.",
            "Standardized style guides and technical glossary across corporate documentation platforms.",
            "Collaborated directly with software engineers to document new software features."
        ]
    },
    "Financial Analyst": {
        "skills": ["Financial Modeling", "Financial Analysis", "Excel", "VBA", "Bloomberg Terminal", "Valuation", "Accounting", "Corporate Finance", "Power BI", "Forecasting", "CFA"],
        "titles": ["Financial Analyst", "Senior Corporate Finance Analyst", "Investment Analyst"],
        "education": ["BS in Finance", "MS in Quantitative Finance", "CFA Level II Candidate"],
        "companies": ["Capital Investments", "Global Wealth Management", "WallStreet Analytics", "FinancePros"],
        "responsibilities": [
            "Built discounted cash flow (DCF) models and valuation reports for M&A target acquisitions.",
            "Developed automated financial consolidation and budgeting models in Excel VBA.",
            "Analyzed quarterly revenue variances and delivered financial forecast reports to CFO.",
            "Evaluated corporate capital expenditure proposals and ROI metrics."
        ]
    },
    "Accountant": {
        "skills": ["Accounting", "Bookkeeping", "General Ledger", "Taxation", "Financial Statements", "QuickBooks", "SAP", "Excel", "Auditing", "CPA", "Accounts Payable", "Reconciliation"],
        "titles": ["Senior Accountant", "Staff Accountant", "Financial Accountant", "Tax Auditor"],
        "education": ["BS in Accounting", "CPA License", "MS in Taxation"],
        "companies": ["Accountability Partners", "Precision Ledger", "TaxShield LLC", "Apex Audit"],
        "responsibilities": [
            "Prepared monthly balance sheets, income statements, and cash flow financial reports.",
            "Managed full-cycle accounts payable, receivable, and bank reconciliations in QuickBooks.",
            "Ensured compliance with GAAP accounting standards and state tax regulations.",
            "Coordinated annual external audit procedures and documentation requests."
        ]
    },
    "Human Resources Manager": {
        "skills": ["Human Resources", "Recruitment", "Employee Relations", "Onboarding", "HRIS", "Performance Management", "Payroll", "Talent Acquisition", "Labor Laws", "SHRM-CP"],
        "titles": ["Human Resources Manager", "HR Generalist", "People Operations Director"],
        "education": ["BS in Human Resources", "MS in Organizational Leadership", "SHRM-CP Certified"],
        "companies": ["PeopleFirst Corp", "TalentPulse", "HumanCapital Solutions", "Workplace Dynamics"],
        "responsibilities": [
            "Oversee HR operations, employee benefit administration, and company performance reviews.",
            "Developed corporate onboarding and training programs for over 200 new hires.",
            "Handled employee relations conflict resolution while ensuring full labor law compliance.",
            "Administered HRIS platforms (Workday/BambooHR) for personnel records and payroll."
        ]
    },
    "Technical Recruiter": {
        "skills": ["Recruitment", "Talent Acquisition", "Technical Sourcing", "LinkedIn Recruiter", "Boolean Search", "Screening", "Applicant Tracking System (ATS)", "Interviewing", "Negotiation"],
        "titles": ["Technical Recruiter", "Senior IT Recruiter", "Talent Acquisition Specialist"],
        "education": ["BS in Communications", "BS in Business", "Certified Recruiter"],
        "companies": ["TalentForge Staffing", "TechRecruiters Inc.", "Global Talent Search", "HireSmart"],
        "responsibilities": [
            "Sourced, interviewed, and placed software engineers, cloud architects, and data scientists.",
            "Utilized advanced Boolean search syntax on LinkedIn Recruiter and GitHub to source candidates.",
            "Managed candidate pipeline workflows in Greenhouse ATS and Lever.",
            "Negotiated salary packages and job offers with prospective technical candidates."
        ]
    },
    "Digital Marketing Specialist": {
        "skills": ["Digital Marketing", "SEO", "SEM", "Google Ads", "Google Analytics", "Social Media Marketing", "Content Marketing", "Email Marketing", "Copywriting", "HubSpot", "PPC"],
        "titles": ["Digital Marketing Specialist", "Growth Marketing Lead", "SEO / PPC Strategist"],
        "education": ["BS in Marketing", "Google Ads Certified", "HubSpot Content Marketing Certificate"],
        "companies": ["GrowthEngine Agency", "DigitalDrive Media", "ReachGlobal Marketing", "VibeDigital"],
        "responsibilities": [
            "Managed $50,000 monthly Google Ads and Meta social media PPC ad campaigns.",
            "Executed technical SEO keyword optimization strategy boosting organic traffic by 60%.",
            "Designed automated email marketing nurture workflows in HubSpot.",
            "Analyzed conversion funnels and user acquisition campaigns in Google Analytics 4."
        ]
    },
    "Content Strategist": {
        "skills": ["Content Strategy", "Copywriting", "Content Marketing", "Blogging", "SEO Writing", "Social Media", "Editing", "WordPress", "Content Management", "Brand Voice"],
        "titles": ["Content Strategist", "Senior Copywriter", "Content Marketing Manager"],
        "education": ["BA in Journalism / English", "MA in Marketing Communications"],
        "companies": ["ContentWorks", "Storyline Media", "WordCraft Agency", "BrandVoice Studio"],
        "responsibilities": [
            "Formulated editorial content strategy and published 100+ SEO-optimized blog articles.",
            "Authored marketing whitepapers, case studies, and email copy driving lead generation.",
            "Managed WordPress publishing calendar and social media distribution.",
            "Maintained consistent brand messaging across all digital touchpoints."
        ]
    },
    "Sales Executive": {
        "skills": ["Sales", "B2B Sales", "Lead Generation", "CRM", "Salesforce", "Account Management", "Negotiation", "Cold Calling", "Closing", "Business Development", "Prospecting"],
        "titles": ["Sales Executive", "Account Executive", "Business Development Manager"],
        "education": ["BS in Business Administration", "BS in Sales & Marketing"],
        "companies": ["Apex Sales Solutions", "GlobalTech Sales", "RevenueGrowth Corp", "PrimeVend"],
        "responsibilities": [
            "Generated $1.5M in annual B2B software sales revenue across enterprise accounts.",
            "Managed full sales cycle from initial cold prospecting outreach to contract closing.",
            "Maintained accurate sales pipeline forecasts and customer logs in Salesforce CRM.",
            "Delivered persuasive product sales demonstrations to C-level executives."
        ]
    }
}

FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris"]

def generate_resume_text(category, config, index):
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    full_name = f"{first_name} {last_name}"
    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(10, 99)}@gmail.com"
    phone = f"+1 ({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"
    
    title = random.choice(config["titles"])
    edu = random.choice(config["education"])
    company = random.choice(config["companies"])
    
    selected_skills = random.sample(config["skills"], k=min(len(config["skills"]), random.randint(7, 12)))
    resp_sample = random.sample(config["responsibilities"], k=3)
    
    years_exp = random.randint(3, 12)
    
    resume_text = f"""{full_name}
{title} | {email} | {phone} | Location: San Francisco, CA

PROFESSIONAL SUMMARY
Results-driven {title} with {years_exp}+ years of experience in {category} roles. Proven track record at {company} delivering high-impact solutions. Adept in {', '.join(selected_skills[:4])}.

SKILLS & CORE COMPETENCIES
{', '.join(selected_skills)}

WORK EXPERIENCE
{title} - {company} (2020 - Present)
- {resp_sample[0]}
- {resp_sample[1]}
- {resp_sample[2]}

Previous Role - Tech Solutions Inc (2016 - 2020)
- Worked extensively on project deliverables utilizing {selected_skills[0]} and {selected_skills[1]}.
- Collaborated with cross-functional teams to improve operational efficiency by 20%.

EDUCATION
{edu} - State University (Graduated 2016)

PROJECTS & CERTIFICATIONS
- Project: Built automated system utilizing {selected_skills[0]} and {selected_skills[2]}.
- Certification: Certified Specialist in {category} & {selected_skills[0]}
"""
    return resume_text.strip()

def main():
    os.makedirs(DATASET_DIR, exist_ok=True)
    rows = []
    
    # Generate 24 resumes for each of the 25 categories (Total: 600 resumes)
    resumes_per_category = 24
    for cat_name, config in CATEGORIES_CONFIG.items():
        for i in range(resumes_per_category):
            text = generate_resume_text(cat_name, config, i)
            rows.append({"category": cat_name, "resume_text": text})
            
    random.shuffle(rows)
    
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["category", "resume_text"])
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Dataset generated successfully at {CSV_PATH}. Total rows: {len(rows)}")

if __name__ == "__main__":
    main()
