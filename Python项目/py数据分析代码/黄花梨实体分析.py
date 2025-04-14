# 从aip中导入AipNlp
from aip import AipNlp
import requests
import json

""" 你的 APPID AK SK """
APP_ID = "6579093"
API_KEY = "kiIQTamnxbWwlVaBMPoMejXx"
SECRET_KEY = "CU8S4GH2k6Mpi5WzyrA36IpcXxYp64yf"

# 生成客户端，并将结果存储在client中
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


class HuanghualiClassifier:
    def __init__(self):
        self.access_token = self._get_access_token()
        self.material_keywords = ['原木', '板料', '树头', '老料']  # 原材料关键词
        self.craft_keywords = ['雕', '手串', '摆件', '印章']     # 工艺品关键词
        self.furniture_keywords = ['桌', '椅', '柜', '床']      # 家具关键词

    def _get_access_token(self):
        """获取访问令牌"""
        url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}'
        response = requests.post(url)
        return response.json().get('access_token')

    def _entity_analysis(self, text):
        """调用实体分析接口"""
        url = f'https://aip.baidubce.com/rpc/2.0/nlp/v1/entity_analysis?access_token={self.access_token}'
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({'text': text[:128]})  # 截断前128个字符
        response = requests.post(url, headers=headers, data=payload)
        return response.json()

    def _classify_by_entity(self, entity_data):
        """
        分类决策逻辑（优先级从高到低）：
        1. 实体概念层级分析
        2. 实体描述关键词匹配
        3. 原始文本关键词匹配
        """
        text = entity_data.get('text', '')
        
        # 遍历所有识别到的实体
        for entity in entity_data.get('entity_analysis', []):
            # 优先使用LINKED的实体
            if entity.get('status') == 'LINKED':
                category = entity.get('category', {})
                desc = entity.get('desc', '')
                
                # 根据百科分类判断
                if '家具' in category.get('level_2', ''):
                    return '家具'
                if '工艺' in category.get('level_2', '') or '手工艺品' in category.get('level_3', ''):
                    return '工艺品'
                if '植物' in category.get('level_1', '') and '木材' in category.get('level_2', ''):
                    return '原材料'
                
                # 根据描述内容判断
                if any(kw in desc for kw in self.material_keywords):
                    return '原材料'
                if any(kw in desc for kw in self.craft_keywords):
                    return '工艺品'
                if any(kw in desc for kw in self.furniture_keywords):
                    return '家具'

        # 未匹配到实体时的后备方案
        if any(kw in text for kw in self.material_keywords):
            return '原材料'
        if any(kw in text for kw in self.craft_keywords):
            return '工艺品'
        if any(kw in text for kw in self.furniture_keywords):
            return '家具'
        
        return '未知'

    def classify_product(self, text):
        """完整分类流程"""
        entity_data = self._entity_analysis(text)
        return self._classify_by_entity(entity_data)

# 使用示例
if __name__ == "__main__":
    classifier = HuanghualiClassifier()
    
    test_cases = [
        "海南黄花梨独板平头案",          # 家具
        "越南黄花梨老料直径30cm",       # 原材料 
        "明清风格黄花梨透雕螭龙纹笔筒", # 工艺品
        "海南黄花梨二膘料",            # 原材料
        "黄花梨螭龙纹圈椅"             # 家具
    ]
    
    for text in test_cases:
        category = classifier.classify_product(text)
        print(f"文本：{text}\n分类：{category}\n{'-'*30}")
