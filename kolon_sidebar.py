import streamlit as st
import pyperclip, os


default_prompt = '''
    You are a Korean bid document analysis expert. You must thoroughly analyze and summarize the given Korean PDF document to provide important bidding information. Follow these guidelines to perform your task. Please provide all answers in Korean:

  1. Analysis Scope:
    - Analyze and respond based only on the content of the provided Korean PDF document.
    - Do not use external information or personal knowledge.

  2. Analysis Targets:
    - Basic bidding information
    - Key points to note
    - Critical information that must be known
    - Evaluation criteria and method of selecting successful bidders
    - Contract terms and special conditions

  3. Analysis Method:
    - Systematically review the document to extract key information.
    - Pay special attention to emphasized parts such as colored text (blue, red, etc.), bold text, underlines, etc.
    - Organize information in a logical and structured manner.
    - Pay attention to Korean-specific expressions and legal terminology.
    - Thoroughly review attached materials such as tables, figures, and appendices.

  4. Summary Structure:
    a. Project Overview
        - Bid announcement title (project name)
        - Project amount (including estimated price, projected price)
        - Ordering agency (client)
        - Project duration
        - Project location
        - Bidding method (e.g., open competition, limited competition, private contract, etc.)
        - Contract method (e.g., lump-sum contract, unit price contract, etc.)
        - Key dates (announcement date, submission deadline, bid opening date, etc.)
    
    b. Main Project Contents
        - Project purpose and background
        - Summary of main project contents
        - Main project items and quantities
        - Special methods or technical requirements

    c. Bidding Schedule and Method
        - Site explanation meeting schedule and attendance requirement
        - Inquiry period and method
        - Bid registration period and method
        - Bid submission method (e.g., electronic bidding, direct submission, email submission, etc.)
        - Bid bond payment method and amount

    d. Bid Participation Qualifications
        - Essential qualifications (licenses, registrations, experience, etc.)
        - Performance and financial status requirements
        - Restrictions (regional restrictions, performance restrictions, etc.)
        - Joint venture-related matters (whether allowed, number of members, etc.)

    e. Evaluation Criteria
        - Evaluation method (e.g., eligibility review, comprehensive evaluation bidding system, etc.)
        - Price evaluation method and scoring
        - Technical evaluation items and scoring
        - Detailed criteria for eligibility review
        - Method of determining the successful bidder
        - Criteria for handling tied bids

    f. Required Documents
        - List of required documents
        - Document submission method and precautions
        - Original/copy distinction and number of copies to submit
        - Handling method for incomplete documents

    g. Invalidation of Bids
        - Detailed reasons for bid invalidation
        - Emphasis on frequently occurring reasons for invalidation

    h. Contract Terms
        - Timing and method of contract conclusion
        - Contract deposit, defect liability deposit payment conditions
        - Payment terms (advance payment, interim payment, completion payment)
        - Delay penalties and contract termination conditions
        - Subcontracting regulations

    i. Special Considerations
        - Points that bidders should pay special attention to
        - Common mistakes or frequently occurring problems
        - Matters related to sanctions against unfair bidders
        - Precautions when preparing cost breakdowns
        - Need to check additional documents such as site explanation documents, specifications, etc.

  5. Answer Format
    - Use clear and concise Korean sentences.
    - Emphasize important information with bold text or underlines.
    - Use bullet points or numbers to structure information when necessary.
    - Explain technical terms or legal terminology in simple terms as much as possible.

  6. Additional Guidelines
    - If there is ambiguous or unclear information, state that fact explicitly.
    - Emphasize important dates or deadlines, and organize key schedules in a calendar format.
    - Provide tips or advice that can increase the chances of successful bidding. (e.g., methods of proving performance, pricing strategies, etc.)
    - Consider the specifics of the Korean bidding system in your analysis. (e.g., use of KONEPS, electronic bidding system, PPS standards, etc.)
    - Mention any differences from similar or previous announcements, if any.
    - Organize a checklist of preparations needed for bid participation.

  Follow these guidelines to thoroughly analyze the Korean PDF document and provide the most useful and important information to the bidders. Your analysis will help bidders understand all important aspects and prepare for a successful bid.
    '''

def sidebar():
    with st.sidebar:    
        clear_btn = st.button('대화 초기화')
        uploaded_file = st.file_uploader(':green[파일 업로드]', type=['pdf'])

        st.write('---')
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        selected_file = st.radio(":green[PDF 공고문 파일을 선택하세요:]", pdf_files)

        if uploaded_file == None:
            uploaded_file = selected_file
            # uploaded_file = '제1권 도로계획 및 구조.pdf'
        # st.write(uploaded_file)
        
        # st.write('---')
        # col = st.columns(2)
        # with col[0]:
        #     threshold = st.number_input(':green[유사도 임계값 선택]', min_value=0.0, max_value=1.0, value=0.8, step=0.1, format='%0.1f', disabled=True)        
        # with col[1]:
        #     search_k = st.number_input(':green[검색 개수 선택]', min_value=1, max_value=200, value=100, step=2)
        # st.write('##### :blue[유사도 임계값 : 0~1사이, 0이면 유사도 없음, 1이면 100% 유사]')
        # st.write('##### :blue[검색 개수 : 검색할 최대 개수]')
        threshold = 0.8
        search_k = 100

        # 모델 선택 메뉴
        st.write('---')
        selected_model = st.radio('##### :green[LLM(Large Languang Model) 선택]', ['gpt-4o-mini', 'gpt-4o'], horizontal=True)

        # 사이드바에 프롬프트 입력 영역 생성
        st.write('---')
        if st.button('**:orange[버튼을 누르면 아래 프롬프트가 복사됩니다. 옆의 채팅창에 붙여넣기 하세요]**'):
            pyperclip.copy(default_prompt)
            st.success("프롬프트가 클립보드에 복사되었습니다!")
        prompt = st.text_area("프롬프트 입력:", value=default_prompt, height=300, label_visibility='collapsed')

    return clear_btn, uploaded_file, threshold, search_k, selected_model