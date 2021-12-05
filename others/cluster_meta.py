"""
{
  'clock': {  # 天数时钟信息
    'totaltimeinphase': '150',  # 当前阶段总时间
    'cycles': '748',  # 天数循环次数，从0开始，所以是 实际天数 - 1，现在已经第749天了
    'phase': 'day',  # 当前阶段
    'remainingtimeinphase': '149.01870727539',  # 当前阶段剩余时间
    'mooomphasecycle': '6',  # 月相循环
    'segs': {  # 当天阶段信息，共16段，每段30s
      'night': '3',
      'day': '5',
      'dusk': '8'
    }
  },
  'seasons': {  # 季节信息
    'premode': 'false',
    'season': 'spring',  # 当前季节
    'elapseddaysinseason': '13', 当前季节已过天数（不包括当天）
    'israndom': {  # 季节时长是否随机
      'summer': 'false',
      'autumn': 'false',
      'spring': 'false',
      'winter': 'false'
    },
    'lengths': {  # 季节天数
      'summer': '15',
      'autumn': '20',
      'spring': '20',
      'winter': '15'
    },
    'remainingdaysinseason': '7',  # 当前季节剩余天数（包括当天）
    'mode': 'cycle',
    'totaldaysinseason': '20',  # 当前季节总天数  有时候对不上，最好用已过天数加剩余天数
    'segs': {
      'summer': {
        'night': '4',
        'day': '11',
        'dusk': '1'
      },
      'autumn': {
        'night': '2',
        'day': '8',
        'dusk': '6'
      },
      'spring': {
        'night': '3',
        'day': '5',
        'dusk': '8'
      },
      'winter': {
        'night': '6',
        'day': '5',
        'dusk': '5'
      }
    }
  }
}
"""
