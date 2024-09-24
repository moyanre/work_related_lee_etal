
##### Some ques are only shown if required



## https://blog.devgenius.io/creating-an-interactive-website-with-streamlit-in-python-95-100-days-of-python-6de2868f916c

import streamlit as st
#import streamlit_scrollable_textbox as stx
from PIL import Image
import base64
import pandas as pd


########################## Functions ###########################################################################################
################################################################################################################################
def one_in_X(perc_risk):
    one_in_y = int(round(100/perc_risk, 0))
    return one_in_y

def absolute_risk_lee(
        df_lee, 
        time_duration_years,
        sex,
        alcohol_drinking,
        lifetime_ave_of_cigarette_smoking_freq,
        lifetime_cigarette_smoking_duration,
        education,
        race,
        family_history_of_head_and_neck_cancer,
        current_age):
    
    '''
    1. df_lee: dataframe of risks from Lee 
    2. time_duration_years: int -- 10 
    3. sex: string -- 'male' OR 'female'
    4. alcohol_drinking: string --  'never or <1 drink/day' OR '1-<3 drinks/day' OR '3+ drinks/day'
    5. lifetime_ave_of_cigarette_smoking_freq: string -- 'never' OR '<=20 cigarettes/day' OR '>20 cigarettes/day'
    6. lifetime_cigarette_smoking_duration: string -- 'never' OR '<=20 years' OR '>20 years'
    7. education: string -- '> high school' OR 'high school' OR '< high school'
    8. race: string -- 'non-Hispanic White' OR 'other'
    9. family_history_of_head_and_neck_cancer: string 'unknown' OR 'no' OR 'yes'
    10. current_age: int -- 60
    '''

    if current_age < 45:
        age_grp = '<45'
    elif current_age >= 45 and current_age <= 49:
        age_grp = '45-49'
    elif current_age >= 50 and current_age <= 54:
        age_grp = '50-54'
    elif current_age >= 55 and current_age <= 59:
        age_grp = '55-59'
    elif current_age >= 60 and current_age <= 64:
        age_grp = '60-64'
    elif current_age >= 65 and current_age <= 69:
        age_grp = '65-69'
    elif current_age >= 70 and current_age <= 74:
        age_grp = '70-74'
    elif current_age >= 75 and current_age <= 79:
        age_grp = '75-79'
    elif current_age >= 80 and current_age <= 84:
        age_grp = '80-84'
    else:
        age_grp = '85+'

    cond_sex = df_lee['Sex']== sex
    cond_alcohol = df_lee['Alcohol Drinking']== alcohol_drinking
    cond_smoke_freq = df_lee['Lifetime Average of Cigarette Smoking Frequency']== lifetime_ave_of_cigarette_smoking_freq
    cond_smoke_duration = df_lee['Lifetime Cigarette Smoking Duration']== lifetime_cigarette_smoking_duration
    cond_education = df_lee['Education']== education
    cond_race = df_lee['Race']== race
    cond_HNC_history = df_lee['Family History of Head and Neck Cancer']== family_history_of_head_and_neck_cancer
    cond_age = df_lee['Current Age']== age_grp

    df = df_lee[cond_sex&cond_alcohol&cond_smoke_freq&cond_smoke_duration&cond_education&cond_race&cond_HNC_history&cond_age].copy()
    df.reset_index(drop=True, inplace=True)

    cols_int = [j for j in df.columns if j.startswith(f'{time_duration_years}-year')]
    
    df = df[cols_int].T.copy()
    df.columns = ['risk_perc']
    df['order'] = [j for j in range(1,len(df)+1)]
    df.loc[f'{time_duration_years}-year OCC and OPC risk (%)','risk_perc'] = df.loc[f'{time_duration_years}-year Oral Cavity Cancer risk (%)','risk_perc']  +  \
                                                                         df.loc[f'{time_duration_years}-year Oropharyngeal Cancer risk (%)','risk_perc']
    df.loc[f'{time_duration_years}-year OCC and OPC risk (%)','order'] = 4.5
    df.sort_values(by=['order'], inplace=True)
    df.drop(columns=['order'], inplace=True)
    df['1_out_of_X'] = df['risk_perc'].apply(one_in_X)

    df.index = [j.replace(' risk (%)', '') for j in df.index]
    df.index = [j.replace(f'{time_duration_years}-year ', '') for j in df.index]
    return df

def set_stage(stage):
    st.session_state.stage = stage

if "stage" not in st.session_state:
    st.session_state.stage = 0

def ethno_race(ethn, racee):
    if ethn == 'No' and racee == 'White':
        out = 'non-Hispanic White'
    else:
        out = 'other'
    return out
################################################################################################################################






################################################################################################################################

st.markdown(
    """<a href="https://www.viomepro.com/">
    <img src="data:image/jpg;base64,{}" style="width:100%; height:100%">
    </a>""".format(
        base64.b64encode(open("Viome_Pro_Logo.jpg", "rb").read()).decode()
    ),
    unsafe_allow_html=True,
)
################################################################################################################################


################################################################################################################################
st.text("")
st.text("")
################################################################################################################################


################################################################################################################################
st.title("Understanding and managing your personal risk factors for oral and throat cancer (Version 2: Based on Lee et al.)")


multi = '''
As your dental healthcare provider, our main goals are to maintain your quality of life and to ensure your safety. Towards this goal, we have developed a first of its kind **AI-driven questionnaire** to calculate your personal risk level as compared to the general population. Based on these findings, we will determine if a more precise molecular screening with the CancerDetect™ saliva test is recommended.

According to the American Cancer Society, the prevalence of oral and throat cancer is expected to increase by almost two thirds by 2035. Unfortunately, current early detection methods are limited, resulting in significant morbidity and mortality as most people are asymptomatic and diagnosed in the late stages of these diseases. However, with new technology emerging, we can now [detect oral and throat cancer](https://www.viomepro.com/) earlier than before, which can help prevent progression to the late stages.

No identifiable information about you is collected in this assessment and your dentist does not receive any direct compensation.  We view this as a major public health initiative and the current data suggests that a few minutes of your time could save your life!

For more information about the test, please visit [viomepro.com](https://www.viomepro.com/) or email OralCarePro@viome.com.
'''
st.markdown(multi)

st.markdown("""<hr style="border-top: dotted 3px;height:2px;border:dashed;color:black;background-color:black;" /> """, unsafe_allow_html=True)
################################################################################################################################


################################################################################################################################
st.markdown("""
<style>
.big-font {
    font-size:27px !important;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Please complete the assessment below <br /> <FONT COLOR=SlateBlue> Click the “?” icon for more information on each question </p>', unsafe_allow_html=True)
################################################################################################################################


#################### Inputs ####################################################################################################
################################################################################################################################
################################################################################################################################

#################### Age #######################################################################################################
################################################################################################################################
age_label = '**What is your age?**'
age_tooltip = ''' TBD
'''
age = st.slider(label = age_label, 
                min_value=18, 
                max_value=120,
                help=age_tooltip,
                #help_icon = 'i'
                )

st.markdown(
"""
<style>
    div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}
    #bui2__anchor > svg{
            width: 32px;
            height: 32px;
        }
</style>
""", unsafe_allow_html=True)
################################################################################################################################


#################### Sex #######################################################################################################
################################################################################################################################
sex_label = '**What is your sex at birth?**'
sex_tooltip = ''' TBD 
'''
sex = st.selectbox(label=sex_label,
                   options = [
                              '-- Select an option --', 
                              'Female', 
                              'Male',
                              'Other'
                             ],
                   help = sex_tooltip)


st.markdown(
"""
<style>
    div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}
    #bui3__anchor > svg{
           width: 32px;
            height: 32px;
        }
</style>
""", unsafe_allow_html=True)

dico_sex = {
            '-- Select an option --': '-- Select an option --',
            'Female': 'female',
            'Male': 'male',
            'Other': 'female'
            }

sex = dico_sex[sex]
################################################################################################################################



# level_two_options = {
#     "Cars" : ["Honda", "Opel", "Tesla"],
#     "Food" : ["Egg", "Pizza", "Spinach"],
#     "Electronics" : ["Headphones", "Laptop", "Phone"]
# }

# #first_choice = "Cars"
# first_choice = st.selectbox("First level options", ["Cars", "Food", "Electronics"])
# second_choice = st.selectbox("Second level options", level_two_options[first_choice])

# st.write("You chose: ", second_choice)


#################### Ethnicity and race #######################################################################################################
################################################################################################################################
ethnicity_label = "**Are you Hispanic or Latino?**" 
ethnicity_tooltip = ''' TBD
'''
ethnicity = st.selectbox(label=ethnicity_label,
                               options = ['-- Select an option --',
                                          'Yes', 
                                          'No'
                                         ],
                               help=ethnicity_tooltip
                               )
st.markdown(
"""
<style>
    div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}
    #bui9__anchor > svg{
            width: 32px;
            height: 32px;
        }
</style>
""", unsafe_allow_html=True)

#########################################################################

if ethnicity == 'No':

    race_label = "**What racial group describes you?**" 
    race_tooltip = ''' TBD
    '''
    race = st.selectbox(label=race_label,
                        options = ['-- Select an option --',
                                    'White', 
                                    'Black or African American',
                                    'Asian',
                                    'Native Hawaiian or Other Pacific Islander',
                                    'American Indian or Alaska Native',
                                    'Other'
                                    ],
                        help=race_tooltip
                                )
    st.markdown(
    """
    <style>
        div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}
        #bui9__anchor > svg{
                width: 32px;
                height: 32px;
            }
    </style>
    """, unsafe_allow_html=True)
else:
    race = 'Not applicable'
################################################################################################################################

#################### Education #######################################################################################################
################################################################################################################################
education_label = '**What is the highest level of school you have completed?**' 
education_tooltip = ''' TBD
'''
education_level = st.selectbox(label=education_label,
                               options = ['-- Select an option --',
                                          'Less than high school', 
                                          'High school',
                                          'More than high school'
                                         ],
                               help=education_tooltip
                               )
st.markdown(
"""
<style>
    div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}
    #bui9__anchor > svg{
            width: 32px;
            height: 32px;
        }
</style>
""", unsafe_allow_html=True)


dico_education = {
                  '-- Select an option --': '-- Select an option --',
                'Less than high school': '< high school',
                'High school': 'high school',
                'More than high school': '> high school'
                }

education_level = dico_education[education_level]
################################################################################################################################


#################### Alcohol ###################################################################################################
################################################################################################################################

## How many alcoholic drinks per week do you consume?

alcohol_label = '**How many alcoholic drinks per week do you consume?**' 
alcohol_tooltip = ''' TBD
'''
alcohol_status = st.selectbox(label=alcohol_label,
                               options = ['-- Select an option --',
                                          'Never or less than 1 drink per day', 
                                          'Between 1 and 2 drinks per day',
                                          'More than 2 drinks per day'
                                         ],
                               help=alcohol_tooltip
                               )
st.markdown(
"""
<style>
    div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}
    #bui9__anchor > svg{
            width: 32px;
            height: 32px;
        }
</style>
""", unsafe_allow_html=True)


dico_alcohol = {
                '-- Select an option --': '-- Select an option --',
                'Never or less than 1 drink per day': 'never or <1 drink/day',
                'Between 1 and 2 drinks per day': '1-<3 drinks/day',
                'More than 2 drinks per day': '3+ drinks/day'
                }

alcohol_status = dico_alcohol[alcohol_status]
################################################################################################################################



#################### cigarette freq and duration ###############################################################################
################################################################################################################################

###################################################################################
cigarette_duration_label = '''**How long have you been smoking cigarette?**'''

tooltip_cigarette_duration = ''' TBD
'''
cigarette_duration_raw = st.selectbox(label = cigarette_duration_label, 
                              options = [
                                         '-- Select an option --',
                                         'Never',
                                         '20 years or less',
                                         'More than 20 years'
                                        ],
                              help=tooltip_cigarette_duration
                                    )
st.markdown(
"""
<style>
    div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}
    #bui6__anchor > svg{
           width: 32px;
            height: 32px;
        }
</style>
""", unsafe_allow_html=True)

dico_cigarette_duration = {
                           '-- Select an option --': '-- Select an option --',
                           'Never': 'never',
                           '20 years or less': '<=20 years',
                           'More than 20 years': '>20 years'
                    }

cigarette_duration = dico_cigarette_duration[cigarette_duration_raw]

###################################################################################

if cigarette_duration in ['<=20 years', '>20 years']:
    cigarette_freq_label = '''**How many cigarettes do you smoke per day?**'''
    tooltip_cigarette_freq = '''TBD
    '''
    cigarette_freq_raw = st.selectbox(label = cigarette_freq_label, 
                                options = [
                                            '-- Select an option --',
                                            '20 or less cigarettes per day',
                                            'More than 20 cigarettes per day'
                                            ],
                                help=tooltip_cigarette_freq
                                        )
    st.markdown(
    """
    <style>
        div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}
        #bui6__anchor > svg{
            width: 32px;
                height: 32px;
            }
    </style>
    """, unsafe_allow_html=True)

    dico_cigarette_freq = {
                        '-- Select an option --': '-- Select an option --',
                        '20 or less cigarettes per day': '<=20 cigarettes/day',
                        'More than 20 cigarettes per day': '>20 cigarettes/day'
                        }

    cigarette_freq = dico_cigarette_freq[cigarette_freq_raw]
elif cigarette_duration == 'never':
    cigarette_freq = 'never'
else: ### i.e. '-- Select an option --'
    cigarette_freq = 'Not applicable'

################################################################################################################################


#################### Family history ############################################################################################
################################################################################################################################
hnc_family_history_label = '**Have your parents, siblings, or children ever been diagnosed with head and neck cancer?**' 
hnc_family_history_tooltip = ''' TBD
'''
hnc_family_history = st.selectbox(label=hnc_family_history_label,
                                  options = ['-- Select an option --',
                                             'Unknown', 
                                             'No',
                                             'Yes'
                                             ],
                                  help=hnc_family_history_tooltip
                               )
st.markdown(
"""
<style>
    div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}
    #bui9__anchor > svg{
            width: 32px;
            height: 32px;
        }
</style>
""", unsafe_allow_html=True)


dico_hnc_family_history = {
                           '-- Select an option --': '-- Select an option --',
                           'Unknown': 'unknown',
                           'No': 'no',
                           'Yes': 'yes'
                          }

hnc_family_history = dico_hnc_family_history[hnc_family_history]
################################################################################################################################


#################### Years of risk  ############################################################################################
################################################################################################################################
years_of_risk_label = '**Number of years to the future for risk computation**' 
years_of_risk_tooltip = ''' TBD
'''
years_of_risk = st.selectbox(label=years_of_risk_label,
                               options = ['-- Select an option --',
                                          '5', 
                                          '10',
                                          '15',
                                          '20',
                                          '25',
                                          '30'
                                         ],
                               help=years_of_risk_label
                               )
st.markdown(
"""
<style>
    div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}
    #bui9__anchor > svg{
            width: 32px;
            height: 32px;
        }
</style>
""", unsafe_allow_html=True)




#years_of_risk = 10
################################################################################################################################


######################## Import Lee data #######################################################################################
################################################################################################################################
df_lee = pd.read_csv('Lee_Absolute_Risks_Cleaned.csv', index_col=0)
df_lee.reset_index(drop=True, inplace=True)
################################################################################################################################





button_label = r"$\textsf{\large Calculate your quantitative risk}$"

if(st.button(button_label, on_click=set_stage, args=(1,))):
    st.session_state.df_lee = df_lee
    st.session_state.sex = sex
    st.session_state.years_of_risk = years_of_risk
    st.session_state.alcohol_status = alcohol_status
    st.session_state.cigarette_duration = cigarette_duration
    st.session_state.cigarette_freq = cigarette_freq
    st.session_state.education_level = education_level
    st.session_state.ethnicity = ethnicity
    st.session_state.race = race
    st.session_state.hnc_family_history = hnc_family_history
    st.session_state.age = age




    if st.session_state.years_of_risk != '-- Select an option --' and st.session_state.alcohol_status != '-- Select an option --' \
          and st.session_state.cigarette_duration != '-- Select an option --' and st.session_state.cigarette_freq != '-- Select an option --' \
            and st.session_state.education_level != '-- Select an option --' and st.session_state.ethnicity != '-- Select an option --' \
                and st.session_state.race != '-- Select an option --' and st.session_state.hnc_family_history != '-- Select an option --':

        
        years_of_risk = int(float(st.session_state.years_of_risk))


        ethnicity_race = ethno_race(st.session_state.ethnicity, st.session_state.race)
        st.session_state.ethnicity_race = ethnicity_race

        df_risks = absolute_risk_lee(df_lee = st.session_state.df_lee, 
                                    time_duration_years = st.session_state.years_of_risk,
                                    sex = st.session_state.sex,
                                    alcohol_drinking = st.session_state.alcohol_status,
                                    lifetime_ave_of_cigarette_smoking_freq = st.session_state.cigarette_freq,
                                    lifetime_cigarette_smoking_duration = st.session_state.cigarette_duration,
                                    education = st.session_state.education_level,
                                    race = st.session_state.ethnicity_race,
                                    family_history_of_head_and_neck_cancer = st.session_state.hnc_family_history,
                                    current_age = st.session_state.age)

        st.session_state.df_risks = df_risks

        risk_OCC_text = f''' 
        :red[1 out of {st.session_state.df_risks.loc['Oral Cavity Cancer','1_out_of_X']}] people with the same risk factor profile as yours would be diagnosed with :red[Oral Cavity Cancer] within {st.session_state.years_of_risk} years.
        '''
        st.session_state.risk_OCC_text = risk_OCC_text

        risk_OPC_text = f''' 
        :red[1 out of {st.session_state.df_risks.loc['Oropharyngeal Cancer','1_out_of_X']}] people with the same risk factor profile as yours would be diagnosed with :red[Oropharyngeal Cancer] within {st.session_state.years_of_risk} years.
        '''
        st.session_state.risk_OPC_text = risk_OPC_text

        risk_HPC_text = f''' 
        :red[1 out of {st.session_state.df_risks.loc['Hypopharyngeal Cancer','1_out_of_X']}] people with the same risk factor profile as yours would be diagnosed with :red[Hypopharyngeal Cancer] within {st.session_state.years_of_risk} years.
        '''
        st.session_state.risk_HPC_text = risk_HPC_text

        risk_Laryngeal_text = f''' 
        :red[1 out of {st.session_state.df_risks.loc['Laryngeal Cancer','1_out_of_X']}] people with the same risk factor profile as yours would be diagnosed with :red[Laryngeal Cancer] within {st.session_state.years_of_risk} years.
        '''
        st.session_state.risk_Laryngeal_text = risk_Laryngeal_text

        risk_OCCandOPC_text = f''' 
        :red[1 out of {st.session_state.df_risks.loc['OCC and OPC','1_out_of_X']}] people with the same risk factor profile as yours would be diagnosed with :red[Oral Cavity and Oropharyngeal Cancers] within {st.session_state.years_of_risk} years.
        '''
        st.session_state.risk_OCCandOPC_text = risk_OCCandOPC_text

        risk_HNC_text = f''' 
        :red[1 out of {st.session_state.df_risks.loc['Head and Neck Cancer','1_out_of_X']}] people with the same risk factor profile as yours would be diagnosed with :red[Head and Neck Cancer] within {st.session_state.years_of_risk} years.
        '''
        st.session_state.risk_HNC_text = risk_HNC_text


        # risk_OCC_text = f''' 
        # 1. Your quantitative risk for :red[Oral Cavity Cancer] is :blue[1 out of {st.session_state.df_risks.loc['Oral Cavity Cancer','1_out_of_X']} people].
        # '''
        # st.session_state.risk_OCC_text = risk_OCC_text

        # risk_OPC_text = f''' 
        # 2. Your quantitative risk for :red[Oropharyngeal Cancer] is :blue[1 out of {st.session_state.df_risks.loc['Oropharyngeal Cancer','1_out_of_X']} people].
        # '''
        # st.session_state.risk_OPC_text = risk_OPC_text

        # risk_HPC_text = f''' 
        # 3. Your quantitative risk for :red[Hypopharyngeal Cancer] is :blue[1 out of {st.session_state.df_risks.loc['Hypopharyngeal Cancer','1_out_of_X']} people].
        # '''
        # st.session_state.risk_HPC_text = risk_HPC_text

        # risk_Laryngeal_text = f''' 
        # 4. Your quantitative risk for :red[Laryngeal Cancer] is :blue[1 out of {st.session_state.df_risks.loc['Laryngeal Cancer','1_out_of_X']} people].
        # '''
        # st.session_state.risk_Laryngeal_text = risk_Laryngeal_text

        # risk_OCCandOPC_text = f''' 
        # 5. Your quantitative risk for :red[Oral Cavity and Oropharyngeal Cancers] is :blue[1 out of {st.session_state.df_risks.loc['OCC and OPC','1_out_of_X']} people].
        # '''
        # st.session_state.risk_OCCandOPC_text = risk_OCCandOPC_text

        # risk_HNC_text = f''' 
        # 6. Your quantitative risk for :red[Head and Neck Cancer] is :blue[1 out of {st.session_state.df_risks.loc['Head and Neck Cancer','1_out_of_X']} people].
        # '''
        # st.session_state.risk_HNC_text = risk_HNC_text

        st.subheader(f'{st.session_state.risk_OCC_text}')
        st.subheader(f'{st.session_state.risk_OPC_text}')
        st.subheader(f'{st.session_state.risk_HPC_text}')
        st.subheader(f'{st.session_state.risk_Laryngeal_text}')
        st.subheader(f'{st.session_state.risk_OCCandOPC_text}')
        st.subheader(f'{st.session_state.risk_HNC_text}')

        ###st.subheader(':blue[Once you obtain the CancerDetect saliva test, we can provide you with a more accurate personal risk assessment.]')

        form = st.form(key='my_form')
        #submitted = form.form_submit_button("Tell me more", on_click=set_stage, args=(2,))
        #submitted = st.button(r"$\textsf{\large Tell me more}$", on_click=set_stage, args=(2,))

    else:
        list_resp = [st.session_state.sex, st.session_state.ethnicity, st.session_state.race, 
                     st.session_state.education_level, st.session_state.alcohol_status, st.session_state.cigarette_freq, 
                     st.session_state.cigarette_duration, st.session_state.hnc_family_history, st.session_state.years_of_risk]
        no_of_misses = 0
        for j in list_resp:
            if j == '-- Select an option --':
                no_of_misses+=1

        if no_of_misses == 1: 
            opt1, opt2 = 'a response', 'question'
        else:
            opt1, opt2 = 'responses', 'questions'
        
        st.subheader(f'Please provide {opt1} to the following {opt2}:')
        num = 1

        if st.session_state.sex == '-- Select an option --':
            mssg = f'{num}. {sex_label}'
            num+=1
            st.write(f'{mssg}')
        if st.session_state.ethnicity == '-- Select an option --':
            mssg = f'{num}. {ethnicity_label}'
            num+=1
            st.write(f'{mssg}')
        if st.session_state.race == '-- Select an option --':
            mssg = f'{num}. {race_label}'
            num+=1
            st.write(f'{mssg}')
        if st.session_state.education_level == '-- Select an option --':
            mssg = f'{num}. {education_label}'
            num+=1
            st.write(f'{mssg}')
        if st.session_state.alcohol_status == '-- Select an option --':
            mssg = f"{num}. {alcohol_label}"
            num+=1
            st.write(f'{mssg}')
        if st.session_state.cigarette_freq == '-- Select an option --':
            mssg = f'{num}. {cigarette_freq_label}'
            num+=1
            st.write(f'{mssg}')
        if st.session_state.cigarette_duration == '-- Select an option --':
            mssg = f'{num}. {cigarette_duration_label}'
            num+=1
            st.write(f'{mssg}')
        if st.session_state.hnc_family_history == '-- Select an option --':
            mssg = f'{num}. {hnc_family_history_label}'
            num+=1
            st.write(f'{mssg}')
        if st.session_state.years_of_risk == '-- Select an option --':
            mssg = f'{num}. {years_of_risk_label}'
            num+=1
            st.write(f'{mssg}')
