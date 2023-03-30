import pandas as pd
from utils.config.common import conf

df = pd.read_pickle(f"{conf.dataPath}cf_base_df.pkl")

class CF_score():
    def __init__(self):
        pass

    def get_cf_score(self, x, y_range, top_k=1, a=0.3978):

        try:
            # sent_to_x (x에게 메시지를 보낸 유저 그룹)
            sent_to_x = df.loc[df['mem_no']==x]['receive_list'].values[0]
            # 추천 리스트 초기화
            score_list = list()
            # number of candidates(RecommendationCandidates) : Top N with PR score
            print(f"Candidate Count : {len(y_range)}")
            # 추천 후보 집단(RecommendationCandidates)의 모든 유저 y에 대해 수행
            for y, score in zip(y_range.index, y_range.values) :
                sent_to_y = df[df['mem_no']==y]['receive_list'].values[0]
                # calculate score x_y
                score_x_y = 0
                for u in sent_to_y :
                    try :
                        u_refrom = df[df['mem_no']==u]['sent_list'].values[0] #u가 메시지를 보낸 유저집단(ReFrom_u)
                        x_refrom = df[df['mem_no']==x]['sent_list'].values[0] #x가 메시지를 보낸 유저집단(ReFrom_x)
                        intersection = list(set(u_refrom) & set(x_refrom)) # ReFrom_u ∩ ReFrom_x
                        union = list(set(u_refrom) | set(x_refrom)) # ReFrom_u ∪ ReFrom_x

                        if len(intersection) == 0 :
                            continue # To avoid zero-division
                        score_x_y += len(intersection) / len(union) # score_x_y <- score_x_y + similarity_x_u

                    except :
                        pass

                # initiate score y_x
                score_y_x = 0
                # x에게 메시지를 보낸 유저 집단 v에 대하여 반복 수행
                for v in sent_to_x :
                    try :
                        v_refrom = df[df['mem_no']==v]['sent_list'].values[0] # v가 메시지를 보낸 유저집단(ReFrom_v)
                        y_refrom = df[df['mem_no']==y]['sent_list'].values[0] # y가 메시지를 보낸 유저집단(ReFrom_y)
                        intersection = list(set(v_refrom) & set(y_refrom))
                        union = list(set(v_refrom) | set(y_refrom))

                        if len(intersection) == 0 :
                            continue # To avoid zero-division
                        score_y_x += len(intersection) / len(union) # score_y_x <- score_y_x + similarity_y_v

                    except :
                        pass

                # Calculate harmonic mean
                if score_x_y != 0 and score_y_x != 0 :
                    harmonic_mean_score = (2 * score_x_y * score_y_x) / (score_x_y + score_y_x)
                else :
                    harmonic_mean_score = 0
                # add weight alpha(default a=0.3978)
                final_score = (score[0] * (1-a)) + (harmonic_mean_score * a)

                score_list.append((y, final_score))  # Recs <- (y, reciprocalScore_x,y)

        except:
            return None

        finally :
            top_k_list = sorted(score_list, key=lambda x : -x[1])[:top_k]
            del sent_to_x, sent_to_y

        return top_k_list[0][0]